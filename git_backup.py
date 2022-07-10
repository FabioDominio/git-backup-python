from git import Repo
from git import RemoteProgress
from models.gitlab import GitlabModel
from pathlib import Path
import shutil
import stat
import datetime
import sys

def redo_with_write(redo_func, path, err):   
    Path(path).chmod(stat.S_IWUSR)
    redo_func(path)

# Read destination folder and API token
if (len(sys.argv) < 2 or len(sys.argv) > 3):
    # Wrong number of arguments
    print("Usage: git_backup.py <api_token> <destination_path>")
    exit(-1)

# Else get the API token
token = sys.argv[1]

if (len(sys.argv) == 3):
    destination = sys.argv[2]
else:
    destination = "."

# Init Gitlab model
model = GitlabModel(token)

# Retrieve the list of namespaces
namespaces = model.getNamespaces()

# Iterate for each namespace
for namespace in namespaces:
    print("Processing namespace \"" + namespace['name'] + "\"...")
    # Create the namespace folder, if not exists
    Path(destination).joinpath(namespace['name']).mkdir(parents=True, exist_ok=True)
    # Retrieve all the repositories for the namespace 
    print("\tRetrieving repositories...")   
    repositories = model.getNamespaceRepositories(namespace['name'])
    # Iterate for each repository
    for repository in repositories:
        print("\tProcessing repository \"" + repository['name'] + "\"...")
        path = Path(destination).joinpath(namespace['name']).joinpath(repository['name'])        
        # Create the repository folder, if not exists    
        path.mkdir(parents=True, exist_ok=True)
        bare_repository_path = path.joinpath("bare")
        non_bare_repository_path = path.joinpath("non_bare")  
        # Delete the source directory folder
        print("\t\tDeleting bare repository folder...")
        if (bare_repository_path.exists()):            
            shutil.rmtree(path=bare_repository_path, onerror = redo_with_write)  
        # Delete the repository directory folder
        print("\t\tDeleting repository folder...")
        if (non_bare_repository_path.exists()):            
            shutil.rmtree(path=non_bare_repository_path, onerror = redo_with_write)        
        bare_repository_path.mkdir(parents=True, exist_ok=True)
        non_bare_repository_path.mkdir(parents=True, exist_ok=True)        
        # Clone mirror the repository
        print("\t\tCloning bare repository...")
        bare_repo = Repo.clone_from(url=repository['url'], to_path=bare_repository_path, mirror=True)
         # Clone the repository
        print("\t\tCloning non bare repository...")
        non_bare_repo = Repo.clone_from(url=repository['url'], to_path=non_bare_repository_path, mirror=False)
        # Backup the repository
        print("\t\tArchiving repository sources...")
        try:
            save_path = path.joinpath(repository['name'] + "_src_" + datetime.date.today().strftime("%Y%m%d") + ".zip")
            with open(save_path, 'wb') as fp:
                bare_repo.archive(fp, format='zip')    
                fp.close()   
        except:
            print("Error archiving repository \"" + repository['name'] + "\" sources")  
        finally:
            # Close repository
            bare_repo.close()      
        # Backup the repository
        print("\t\tArchiving repository...")
        try:
            save_path = path.joinpath(repository['name'] + "_repo_" + datetime.date.today().strftime("%Y%m%d"))
            shutil.make_archive(base_name=save_path, format="zip", root_dir=non_bare_repository_path)             
        except:
            print("Error archiving repository \"" + repository['name'])
        finally:
            # Close repository
            non_bare_repo.close()
        # Delete the source directory folder
        print("\t\tDeleting bare repository folder...")        
        if (bare_repository_path.exists()):            
            shutil.rmtree(path=bare_repository_path, onerror = redo_with_write)  
        # Delete the repository directory folder
        print("\t\tDeleting repository folder...")        
        if (non_bare_repository_path.exists()):            
            shutil.rmtree(path=non_bare_repository_path, onerror = redo_with_write)  