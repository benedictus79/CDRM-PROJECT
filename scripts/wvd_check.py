# Import dependencies
import os
import glob


# Define WVD device check
def check_for_wvd():
    try:

        # Use glob to get the name of the .wvd
        extracted_device = glob.glob(f'{os.getcwd()}/databases/WVDs/*.wvd')[0]

        # Return the device path
        return extracted_device
    except:

        # Check to see if the WVDs folder exist, if not create it
        if 'WVDs' not in os.listdir(fr'{os.getcwd()}/databases'):
            os.makedirs(f'{os.getcwd()}/databases/WVDs')

        # Stop the program and print out instructions
        return None
