### Introduction
The repository adds simple class for adding a wrapper on top of kaggle cli tools for ease of downloading competition datasets, listing competitions, downloading and un-zipping datasets.

It aims to make it easy to use kaggle datasets directly from python scripts. 
 It's main usecase is to be used as a submodule in other repos/ or used as a standalone package.
 If the library is used as a standalone package - the data is downloaded and stored in data folder.
 In case of using the package as a submodule - the data is downloaded in a data folder created in the base folder of the calling script. 

### Installation
The repo relies on setuptools and kaggle library packages. To install the repo please use one of the following options:


```bash
pip install -U kaggle setuptools
python setup.py install
```


It also assumes that presence of Kaggle User ID and public API credentials at 

```
On Windows: C:\Users\<Windows-username>\.kaggle\kaggle.json

Others: ~/. kaggle/kaggle.json
```

After the above steps: the repo can be installed from git using:

```
pip install git+https://github.com/sunny1401/kaggle_utils.git#egg=kaggle-cli-wrapper
```

The project can also be installed using pip:

```
pip install kaggle-cli-wrapper
```

## Code details

### DataAPI class

#### To list all available datasets

```python
from kaggle_cli_wrapper import KaggleDataApi

kda = KaggleDataApi(call_path=__file__)
kda.list_all_kaggle_datasets(search_term="cityscapes")
```
The call_path argument is required to decide the folder where downloaded files are stored.

The function would return all available datasets with cityscape. This would also be saved as a .txt file. 

Currently the list is sorted by "votes".
To change this sorting please use the argument ```sort_by```. Allowed values of sort by are: 

```python
'hottest', 'votes', 'updated', 'active', 'published'
```


#### To list all available competition datasets

```python
from kaggle_cli_wrapper import KaggleDataApi

kda = KaggleDataApi(call_path=__file__)
kda.list_all_kaggle_competitions(search_term="cityscapes")
```

Currently the list is sorted by "earliestDeadline".
To change this sorting please use the argument ```sort_by```. Allowed values of sort by are: 

```python
'grouped', 'prize', 'earliestDeadline','latestDeadline', 'numberOfTeams', 'recentlyCreated'

```

#### To download datasets
```python
from kaggle_cli_wrapper import KaggleDataApi

kda = KaggleDataApi(call_path=__file__)
kda.download_kaggle_dataset(dataset_name="cityscapes_train_val_test", is_competition_dataset=False)
```

To download a competition dataset, is_competition_dataset needs to be set to True


### ScoringAPI

The code currently supports minimum functionality for submission of files to a competition and getting scores for the competition

#### To submit to a competition

```python
from kaggle_utils.kaggle_cli_wrapper import KaggleScoringsApi

kaggle_scoring_api = KaggleScoringsApi(competition_name="facial-keypoints-detection")

kaggle_scoring_api.submit_solution(submissions_file=submission_path, description="facial_keypoint_vanilla_cnn")
kaggle_scoring_api.get_top_scores()
```

## Remaining Issues

- improve error handling 
- allow for saving of stdout






