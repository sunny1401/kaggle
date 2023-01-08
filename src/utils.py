from dataclasses import dataclass
import subprocess
import pandas as pd
import os
import shutil
import zipfile
from typing import List, Optional, Tuple

import git


@dataclass
class KaggleCompetitionDatasets:
    """
    Kaggle competition datasets
    For getting other datasets, please use the list 
    function to get correct dataset name
    """
    list_all_competitions: str = "kaggle competitions list"
    survey_studies: str = "kaggle-survey-2022"
    transfer_learning_food_recognition: str = "transfer-learning-on-food-recognition"
    bike_sharing: str = "bike-sharing-demand"
    facial_keypoints_detection: str = "facial-keypoints-detection"

@dataclass
class KaggleGeneralDatasets:
    """
    Datasets listed here are sorted by maximum votes.
    For getting other datasets, please use the list 
    function to get correct dataset name
    """
    covid_dataset: str = "allen-institute-for-ai/CORD-19-research-challenge"
    nfl_dataset: str = "maxhorowitz/nflplaybyplay2009to2016"


class KaggleDataApi:

    """
    API has functions for listing competition and general datasets, 
    sending in submissions and getting scores of competitions.

    While competition datasets can be listed without a search term, 
    the same cannot be done for general datasets and they 
    require a search term to be listed/downloaded.
    """

    kaggle_list_competition_datasets_command: str = "kaggle competitions list"
    kaggle_list_general_datasets_command: str = "kaggle datasets list"

    def __init__(self, call_path: str) -> None:
        try:
            git_repo = git.Repo(call_path, search_parent_directories=True).working_tree_dir
        except git.exc.InvalidGitRepositoryError:
            git_repo = git.Repo(__file__, search_parent_directories=True).working_tree_dir
            
        self.KAGGLE_DATA_SAVE_LOCATION = os.path.join(
            git_repo,
            "data"
        )

        self._save_path = self.KAGGLE_DATA_SAVE_LOCATION
        self._dataset_file_name = ""
        os.makedirs(self._save_path, exists_ok = True)

    def __read_kaggle_downloaded_dataset_list(
        self, 
        file_path: str, 
        column_names: List, 
        search_term: Optional[str] = None
    ) -> pd.DataFrame:
        
        """
        Helper function to read the downloaded competition list
        """
        df = pd.read_fwf(file_path)
        if not df.shape[0]:
            print(f"No competition dataset found for {search_term}")
        df = df.iloc[1:, :]
        df.columns = column_names
        return df

    def list_all_kaggle_competions(
        self, 
        search_term: Optional[str] = None, 
        sort_by: Optional[str] = "earliestDeadline"
    ) -> pd.DataFrame:

        """
        Function lists all the kaggle competition datasets. It takes in optional arguments:

        Args:
            search_term: if provided dataset, that search term is used for searching the datasets
            sort_by: By default, we use earliestDeadline for sorting teh datasets. Other accepted 
            values are: 
            ['grouped', 'prize', 'earliestDeadline', 'latestDeadline', 'numberOfTeams', 'recentlyCreated']
        """

        allowed_sort_by = {
            'grouped', 'prize', 
            'earliestDeadline', 'latestDeadline', 
            'numberOfTeams', 'recentlyCreated'
        }

        if sort_by not in allowed_sort_by:
            raise ValueError(
                f"sort_by value: {sort_by} is not valid. Allowed values are: \n"
                f"{allowed_sort_by}"
            )

        if search_term:
            kaggle_command = (
                f"{self.kaggle_list_competition_datasets_command} -s {search_term} --sort-by {sort_by}"
            )
            file_save_path = f"kaggle_competition_list_{search_term}.txt"

        else:
            kaggle_command = (
                f"{self.kaggle_list_competition_datasets_command} --sort-by {sort_by}"
            )
            file_save_path = f"kaggle_competition_list.txt"

        file_name = os.path.join(self.KAGGLE_DATA_SAVE_LOCATION, file_save_path)

        if not os.path.exists(file_name):
            with open(file_name, "w") as f:
                subprocess.call(kaggle_command.split(" "), stdout=f)

        column_names = [
            "competition_name", 
            "deadline", "category", 
            "reward", 
            "team_count", 
            "have_you_entered"
        ]
        return self.__read_kaggle_downloaded_dataset_list(
            file_path=file_name,
            column_names=column_names,
            search_term=search_term
        )
        

    @classmethod
    def list_all_kaggle_datasets(self, search_term, sort_by: str = "votes") -> pd.DataFrame:
        """
        List all datasets available for a particular search term.
        Args:
            search_term: str = search and list kaggle datasets related to input search term
            sort_by: str = by default we sort by votes given to a particular dataset. 
            Other sort terms available are: 'hottest', 'votes', 'updated', 'active', 'published'
        
        """

        allowed_sort_by = {'hottest', 'votes', 'updated', 'active', 'published'}

        if sort_by not in allowed_sort_by:
            raise ValueError(
                f"sort_by value: {sort_by} is not valid. Allowed values are: \n"
                f"{allowed_sort_by}"
            )

        file_name = os.path.join(
            self.KAGGLE_DATA_SAVE_LOCATION, 
            f"kaggle_dataset_list_{search_term}.txt"
        )

        if not os.path.exists(file_name):
            with open(file_name, "w") as f:
                dataset_list_command = (
                    f"{self.kaggle_list_general_datasets_command} -s {search_term} --sort-by {sort_by}"
                )
                subprocess.call(dataset_list_command.split(" "), stdout=f)
        
        column_names = [
            "competition_name", 
            "download_count", "votes", 
            "usability_rating", 
            "title", 
            "size",
            "last_updated"
        ]

        return self.__read_kaggle_downloaded_dataset_list(
            file_path=file_name,
            column_names=column_names,
            search_term=search_term
        )

    def download_kaggle_dataset(
        self, 
        dataset_name: str, 
        is_competition_dataset: bool = True
    ) -> str:

        """
        Download existing datasets from kaggle.

        Args:
            dataset_name: str is the name of the dataset to be downloaded.
                It is first assumed to be key name in the dataclass for 
                competitions and general datasets.
                If the dataset_name is not an attribute of the respective dataclass,
                it is then assumed to be the actual name of the dataset to be downloaded.
            is_competition_dataset: Flag indicating if the dataset is a competition dataset

        """
        if is_competition_dataset:
            kaggle_command = "kaggle competitions"
            dataset_class = KaggleCompetitionDatasets

        else:
            kaggle_command = "kaggle datasets"
            dataset_class = KaggleGeneralDatasets

        try:
            dataset_file_name = getattr(dataset_class, dataset_name)

        except AttributeError:
            # TODO - search the name of dataset in existing file list
            # for competitions

            # TODO - add handling wrong name for general datasets
            dataset_file_name = dataset_name

        self._save_path = os.path.join(self._save_path, f"{dataset_file_name}.zip")

        if not os.path.exists(self._save_path):
            command = f"{kaggle_command} download -c {dataset_file_name}".split(" ")

            subprocess.call(command)
            current_location = os.path.join(os.getcwd(), f"{dataset_file_name}.zip")

            if self._save_path != current_location:
                shutil.move(current_location, self._save_path)

        print(f"File downloaded and saved to:   {self._save_path}")
        self._dataset_file_name = dataset_file_name

    def unzip_and_return_folder_details(self) -> Tuple[str]:

        directory_to_save = os.path.join(os.path.split(self._save_path)[0], self._dataset_file_name)

        if not os.path.exists(directory_to_save):
            if not os.path.exists(self._save_path):
                self.download_kaggle_dataset()
            with zipfile.ZipFile(self._save_path, 'r') as zip_ref:
                zip_ref.extractall(directory_to_save)
            os.remove(self._save_path)

        files_extracted = os.listdir(directory_to_save)

        return directory_to_save, files_extracted

