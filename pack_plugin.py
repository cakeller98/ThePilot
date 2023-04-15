import inspect
import os
import zipfile
import pathlib
import configparser
import logging

# set the cwd to the parent of this script
os.chdir(pathlib.Path(__file__).parent.absolute())

# set up logging to console
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

# log a debug message
logging.debug('Start of program')


def quitter(linenumber=None, filename=__file__):

    if linenumber is None:
        linenumber = inspect.currentframe().f_back.f_lineno

    try:
        logging.debug(
            f'\n\n\n-------Imma Quitter {("at line: " + str(linenumber)) if linenumber is not None else " "} in file "...\{pathlib.Path(filename).relative_to(pathlib.Path(filename).parent.parent)}" ------------\n\n\n')
    except Exception as e:
        print(f'Error: {e}')
        quit()
    quit()


def main():

    # config file path
    config_path = pathlib.Path('config.ini').absolute()
    script_path = pathlib.Path(__file__).parent.absolute()

    # use configparser to parse config file
    addon_name, addon_path, init_path, increment = get_config(
        config_path, script_path)
    addon_version = version_incrementer(init_path, increment)

    zip_path = addon_path.joinpath(addon_name + '_' + addon_version + '.zip')

    # create zip file name
    zip_name = addon_path.parent.absolute().joinpath(
        addon_name + '_' + addon_version + '.zip')
    # create zip file
    zip_file = zipfile.ZipFile(zip_name, 'w')

    # change the current working directory to the parent of zip_name

    # add files to zip file
    # lists all files and directories under your src path
    p = pathlib.Path(addon_path).glob('**/*')
    file_paths = [x for x in p if x.is_file()]  # filter for the files only
    for f in file_paths:
        print(
            f'adding {f} to zip file destination:\n\t\t{f.relative_to(addon_path.parent)}')

    for src_ in file_paths:
        zip_file.write(src_, arcname=src_.relative_to(
            addon_path.parent), compress_type=zipfile.ZIP_DEFLATED)

    # close zip file

    zip_file.close()
    logging.debug(f'Zip file created: {zip_name}')
    logging.debug(f'\n\n\n')
    # validate zip file
    zip_file = zipfile.ZipFile(zip_name, 'r')

    # list contents of zip file
    logging.debug(f'Contents of zip file: {zip_name}')
    for file in zip_file.namelist():
        logging.debug(f'\t{file}')

    # close zip file
    zip_file.close()

    # change the current working directory back to the original working directory
    logging.debug('End of program')
    print(f'Zip file created: {zip_name}')
    return "RESULT===>" + str(zip_name.absolute())


def version_incrementer(init_path, increment):
    success, version = increment_version(init_path, increment)

    if success:
        addon_version = version
    else:
        logging.debug('Failed to increment version')
        logging.debug(f'Version: {version}')
        # get the line number of the current line in the file
        quitter(linenumber=inspect.currentframe().f_back.f_lineno)
    return addon_version


def get_config(config_file, script_path):
    if not file_exists(config_file):
        quitter()
    config = configparser.ConfigParser()
    config.read(config_file)

    # get the addon name from the config file
    addon_name = str(config['config']['addon_name'])

    # calculate the path to the addon folder
    addon_path = pathlib.Path(script_path).joinpath(addon_name)
    init_path = addon_path.joinpath('__init__.py')
    increment = tuple(eval(config['config']['increment']))
    return addon_name, addon_path, init_path, increment


def file_exists(config_file):
    if not config_file.exists():
        logging.debug('Config file not found')
        return False
    # else:
    return True

    # parse config file for addon name, amount to increment version by, path to addon, and files to include and exclude


# this is a test -= please reformat this shit


def increment_version(init_path: str, increment=(0, 0, 0)):
    """ takes the init_path which is expecting the path to the main __init__.py file of the plugin
        if the __init__.py exists and contains a properly formatted bl_info dictionary and version tuple
        then if the increment tuple is not (0,0,0) then the version tuple is incremented by the increment tuple   
        otherwise the version tuple is returned as a string

    Args:
        init_path (str)             : the path to the main __init__.py file of the plugin 
        increment (tuple, optional) : Defaults to (0,0,0). The increment tuple to be added to the version tuple. 
                                      Must be a tuple of 3 integers.


    Raises:
        FileNotFoundError   : if the init_path does not exist
        AttributeError      : if the version string was not replaced in the bl_info_dict_string_new
        AttributeError      : if the bl_info_dict_string was not replaced in the init_file_new

    Returns:
        bool: True if the version was incremented and False if the version was not incremented
        str:  the version as a string to be used for naming of the zip package
    """

    # confirm init_path exists
    # if not raise a file not found error

    if not os.path.exists(init_path):
        raise FileNotFoundError(
            f'ERROR: The path "{init_path}" does not exist')
    logging.debug(f'init_path: {init_path} exists')

    do_replace = True
    # else: the path exists
    if increment == (0, 0, 0):
        do_replace = False
    logging.debug(f'do_replace: {do_replace}')

    # open the __init__.py file
    # read the __init__.py file to get the plugin version
    # extract the bl_info dictionary as a string
    # evaluate the dictionary to get the version tuple

    with open(init_path, 'r+') as f:

        # read the __init__.py file to get the plugin version
        init_file = f.read()
        # find the dictionary bl_info
        start = init_file.find('bl_info')
        end = init_file.find('}', start) + 1

        logging.debug(f'\n\n\t-----init_file begin-------\n\n{init_file}'[
                      0:end + 1] + '\n\n\t-----init_file trunc-------\n\n')

        # extract the bl_info dictionary as a string
        bl_info_dict_string = init_file[start:end]

        # evaluate the dictionary to get the version tuple
        bl_info_dict = eval(bl_info_dict_string.strip('bl_info = '))
        version = bl_info_dict['version']
        version_new = inc_ver(version, increment)

        version_string = f'"version": ({version[0]}, {version[1]}, {version[2]}),'
        version_string_new = f'"version": ({version_new[0]}, {version_new[1]}, {version_new[2]}),'

        if do_replace is False:
            f.close()
            return False, version_string

        # increment the version tuple by the increment tuple
        bl_info_dict_string_new = bl_info_dict_string.replace(
            version_string, version_string_new)

        if version_string in bl_info_dict_string_new:
            raise AttributeError(
                f'ERROR: The version string "{version_string}" was not replaced with "{version_string_new}"')

        init_file_new = init_file.replace(
            bl_info_dict_string, bl_info_dict_string_new)

        if bl_info_dict_string in init_file_new:
            raise AttributeError(
                f'ERROR: The bl_info dictionary string "{bl_info_dict_string}" was not replaced with "{bl_info_dict_string_new}"')

        f.seek(0)
        f.write(init_file_new)
        f.close()

        # return the version string as the new version tuple in the same format as the bl_info dictionary
        version_string_new = f'{version_new[0]}.{version_new[1]}.{version_new[2]}'
        return True, version_string_new


def inc_ver(ver=(0, 0, 0), inc=(0, 0, 1)):
    """ Simple function to add the increment to the version number
        and return it as a tuple
        by default, the version's revision only is incremented by 1

    Args:
        ver (tuple, optional): _description_. Defaults to (0,0,0).
        inc (tuple, optional): _description_. Defaults to (0,0,1).

    Returns:
        tuple: returns a tuple of the incremented version number (maj, min, rev)
    """
    version_new = []
    for i in range(len(ver)):
        version_new.append(ver[i] + inc[i])

    return tuple(version_new)


if __name__ == '__main__':
    main()
    logging.info('Done')
