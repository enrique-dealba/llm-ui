code_text = '''"""Catalog Maintenance Objective."""
# Standard Library Imports
from datetime import datetime, timedelta

# Third Party Imports
from eci2coe import eci2coe
from getPeriod import getPeriod
from commonModelStateVectorToNumpy import commonModelStateVectorToNumpy
from objective_base_class import Objective, State
from calc_collect_value_with_default_params import calc_collect_value_with_default_params
from utils import getRSOOrbitalRegimes, isVisible

class CatalogMaintenanceObjective(Objective):
    """Catalog Maintenance Objective Class."""

    def __init__(
        self,
        sensor_name: str,
        data_mode: str,
        classification_marking: str,
        patience_minutes: int = 30,
        end_time_offset_minutes: int = 20,
        objective_name: str = "Catalog Maintenance Objective",
        objective_start_time: datetime = None,
        objective_end_time: datetime = None,
        priority: int = 10,
    ):
        """Creates a Catalog Maintenance Objective, based on the SNARE algorithm.

        References:
            #. :cite:t:`carden2021snare`

        Args:
            sensor_names (str): String Names of Sensor to perform Catalog Maintenance with.
            data_mode (str): String type for the Machina Common DataModeType being generated.
            classification_marking (str): Classification level of objective intents.
            patience_minutes (int): Amount of time to wait until it's assumed a `SENT` intent failed. Defaults to 30 minutes.
            end_time_offset_minutes (int): amount of minutes into the future to let astroplan schedule an intent. Defaults to 20 minutes.
            objective_name (str, optional): the common name for this objective. Defaults to "Catalog Maintenance Objective".
            objective_start_time (datetime): The earliest time when the objective should begin execution. Defaults to utcnow().
            objective_end_time: (datetime) = The earliest time when the objective should begin execution. Defaults Never!
            priority (int): Astroplan Scheduler Priority, defaults to 9.
        """
        # Set the objective end time... if you want to :)
        if isinstance(objective_end_time, str):
            if objective_end_time.endswith("Z"):
                objective_end_time = datetime.fromisoformat(objective_end_time[:-1])
            else:
                objective_end_time = datetime.fromisoformat(objective_end_time)

        super().__init__(
            data_mode=data_mode,
            classification_marking=classification_marking,
            objective_name=objective_name,
            objective_start_time=objective_start_time,
            objective_end_time=objective_end_time,
        )

        print(
            f"Creating Catalog Maintenance Objective: {self.objective_name}, for sensor {sensor_name}"
        )

        # print(f"Objective {self.objective_name} tracking orbital regimes {orbital_regimes}")

        # Some values to persist
        self.sensor_name = sensor_name
        self.patience_seconds = patience_minutes * 60
        self.end_time_offset_minutes = end_time_offset_minutes
        self.priority = priority

    def run_objective_step(self):
        """The objective step of the Catalog Maintenance Objective."""
        # Step 1: query the belief state for all the needed info
        # Step 1.1: Get all RSO in the belief state.
        rso_ephem_list = self.belief_state.get_from_belief_state(
            model_name="rso",
            sort_asc=True,
            filters=[],
        )

        if len(rso_ephem_list) == 0:
            # Only Run if there are RSO to task against.
            print("No RSO found in the belief state.")
            return

        # [TODO]: Implement after common model update

        # load sensor
        sensor_model = self.getSensorFromBeliefState(self.sensor_name)
        if sensor_model is None:
            print(
                "Cannot run this objective without a sensor model loaded in belief state, aborting..."
            )
            self.current_state = State.TERMINATED
            return

        # Do some math to figure out the "revisit" time, considering future intents
        collect_value_dict = {}

        catalog_id_list = [rso.catalog_id for rso in rso_ephem_list]
        print(f"Retrieved the following RSO: {catalog_id_list}")

        # Get our times
        right_now = datetime.utcnow()
        end_time = right_now + timedelta(minutes=self.end_time_offset_minutes)

        for rso in rso_ephem_list:
            # Step 1.3: Get all Observations (NOT SkyImagery) from the last 24 hours
            # [TODO]: Filter based on the specific RSO in question
            observation_list = self.belief_state.get_from_belief_state(
                model_name="ob",
                sort_asc=True,
                sort_by="createdAt",
                filters=["targets.rso.catalogId = '" + str(rso.catalog_id) + "'"],
            )

            # Get all of the future intents for this RSO
            # print(f"Querying belief state for future intents related to RSO {rso.catalog_id}")
            intents_list = self.get_intents_for_rso(rso=rso)

            # Assign a zero value if future intents exist
            intent_list_length = len(intents_list)
            print(f"{intent_list_length} future Intents found for RSO {rso.catalog_id}")

            # [TODO]: Remove once there aren't old sent intents
            if intent_list_length != 0:
                # Don't worry about sent intents more that 30 minutes ago
                for intent in intents_list:
                    if intent.current_status == "SENT":
                        updated_time = datetime.fromisoformat(intent.updated_at[:-1])
                        if (right_now - updated_time).total_seconds() > self.patience_seconds:
                            intents_list.remove(intent)

            # If there's still a subset of intents, don't make another one
            if intent_list_length != 0:
                collect_value_dict[rso.catalog_id] = 0
                continue

            # Check if the RSO is visible in the planning window
            visibility = isVisible(
                rso=rso, sensor=sensor_model, start_datetime=right_now, end_datetime=end_time
            )

            # Only do our math if we think we can see the thing
            if not visibility:
                collect_value_dict[rso.catalog_id] = 0
                continue

            # Cut down the lists for just the last 24 hours
            down_selected_observation_list = []
            for observation in observation_list:
                yesterday = right_now - timedelta(hours=24)
                if (
                    datetime.fromisoformat(observation.ob_time[:-1]) - yesterday
                ).total_seconds() > 0.0:
                    down_selected_observation_list.append(observation)

            # [TODO]: filter EOObs into tracks (based on collect)
            number_of_tracks_last_24_hours = len(down_selected_observation_list)
            if number_of_tracks_last_24_hours == 0:
                collect_value_dict[rso.catalog_id] = 1
                continue

            last_track_time_seconds = (
                right_now - datetime.fromisoformat(down_selected_observation_list[-1].ob_time[:-1])
            ).total_seconds()
            last_track_hours = last_track_time_seconds / 3600

            # Step 2: calculate orbital parameters of newest ephemeris
            # Handle TLETargets
            if rso.targets[-1].model_type == "TLETarget":
                mean_motion = float(rso.targets[0].line2[52:63])
                first_deriv_mean_motion = float(rso.targets[0].line1[33:43])
                eccentricity = float("0." + rso.targets[0].line2[26:33])

            # Handle StateVectorTargets
            elif rso.targets[-1].model_type == "StateVectorTarget":
                state_vectors = rso.targets[-1].state_vectors
                sorted_state_vectors = sorted(
                    state_vectors,
                    key=lambda x: datetime.fromisoformat(x.timestamp[:-1]),
                )
                last_state_vector = sorted_state_vectors[-1]
                state_vector, _ = commonModelStateVectorToNumpy(last_state_vector)
                mean_motion = 1 / getPeriod(state_vector)
                first_deriv_mean_motion = 0.0
                eccentricity = eci2coe(state_vector)[1]

            # Calculate collect values for each RSO
            collect_value_dict[rso.catalog_id] = calc_collect_value_with_default_params(
                r_time_since_last_track=timedelta(hours=last_track_hours),  # R (timedelta)
                o_number_of_tracks_last_24_hours=number_of_tracks_last_24_hours,  # O ("Oh")
                mean_motion=mean_motion,
                first_deriv_mean_motion=first_deriv_mean_motion,
                eccentricity=eccentricity,
            )

        print("Collect Values:", collect_value_dict)
        winner = max(collect_value_dict, key=collect_value_dict.get)

        # Turn RSO list into dictionary
        rso_dict = {}
        for rso in rso_ephem_list:
            rso_dict[int(rso.catalog_id)] = rso

        # Make an new intent for the winner!
        winning_rso = rso_dict[int(winner)]
        print(f"Winning RSO: {winner} with collect value {collect_value_dict[winner]}")

        # Only schedule non-zero collect value RSO
        if collect_value_dict[winner] > 0.0:
            # Step 3: Calculate orbital regime for each RSO
            orbital_regime_dict = getRSOOrbitalRegimes(rso_ephem=[winning_rso])

            # [TODO]: Make this multi-sensor but not every sensor
            new_intent = self.create_intent(
                target=winning_rso.targets[-1],
                sensor_name=self.sensor_name,
                priority=self.priority,
                num_frames=orbital_regime_dict[int(winner)]["num_frames"],
                integration_time=orbital_regime_dict[int(winner)]["integration_time"],
                latest_end_time=end_time,
            )

            print(
                f"Submitting new Intent for RSO {winner} with collect value {collect_value_dict[winner]}"
            )

            # Push it to the belief state
            self.belief_state.add_to_belief_state(model_name="intent", data_to_add=new_intent)

'''