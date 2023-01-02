### Introduction
The repository adds simple class for adding a wrapper on top of kaggle cli tools for ease of downloading competition datasets, listing competitions, saving and zipping results in data folder, submission of results and getting scores for submissions. 

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

### Code details

~ TODO