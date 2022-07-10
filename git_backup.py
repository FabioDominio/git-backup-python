from git import Repo
from git import RemoteProgress
from models.bitbucket import BitbucketModel
from models.gitlab import GitlabModel
from pathlib import Path
import shutil
import stat
import datetime
import sys
import argparse

def redo_with_write(redo_func, path, err):   
    Path(path).chmod(stat.S_IWUSR)
    redo_func(path)

# Declare argument parser
parser = argparse.ArgumentParser(description='Backup all git repositories.')
parser.add_argument('--service', dest='service', help='the git service provider', required=True, choices=['bitbucket', 'gitlab'])
parser.add_argument('service', nargs=1)
parser.add_argument('--username', dest='username', help='the git username')
parser.add_argument('username', nargs='?')
parser.add_argument('--password', dest='password', help='the git password')
parser.add_argument('password', nargs='?')
parser.add_argument('--apy_key', dest='apikey', help='the git API key')
parser.add_argument('apykey', nargs='?')
parser.add_argument('--destination', dest='destination', help='the repositories clone destination', default='.', required=False)

args = vars(parser.parse_args(sys.argv))

# Else get the API token
model = args['service']
token = args['apykey']
username = args['username']
password = args['password']
destination = args['destination']

# Init Gitlab model
if model == 'gitlab':
    model = GitlabModel(token=token, username=username, password=password)
elif model == 'bitbucket':
    model = BitbucketModel(token=token, username=username, password=password)
else:
    model = None

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
        bare_repo = None
        non_bare_repo = None
        try:     
            # Clone mirror the repository
            print("\t\tCloning bare repository...")
            bare_repo = Repo.clone_from(url=repository['url'], to_path=bare_repository_path, mirror=True)
            # Backup the repository
            print("\t\tArchiving repository sources...")
            try:
                save_path = path.joinpath(repository['name'] + "_src_" + datetime.date.today().strftime("%Y%m%d"))
                #with open(save_path, 'wb') as fp:
                #    bare_repo.archive(fp, format='zip')    
                #    fp.close()
                shutil.make_archive(base_name=save_path, format="zip", root_dir=bare_repository_path)    
            except:
                print("Error archiving repository \"" + repository['name'] + "\" sources")
            finally:
                # Close repository
                bare_repo.close()          
        except:
            print("Error cloning repository \"" + repository['name'] + "\" sources")        
        try:
            # Clone the repository
            print("\t\tCloning non bare repository...")
            non_bare_repo = Repo.clone_from(url=repository['url'], to_path=non_bare_repository_path, mirror=False)
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
        except:
            print("Error cloning bare repository \"" + repository['name'] + "")  
            
        # Delete the source directory folder
        print("\t\tDeleting bare repository folder...")        
        if (bare_repository_path.exists()):            
            shutil.rmtree(path=bare_repository_path, onerror = redo_with_write)  
        # Delete the repository directory folder
        print("\t\tDeleting repository folder...")        
        if (non_bare_repository_path.exists()):            
            shutil.rmtree(path=non_bare_repository_path, onerror = redo_with_write)  