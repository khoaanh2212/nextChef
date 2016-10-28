import random
import string


def random_string(length, alphabet=None):
    """
    Given a length generates a random string (lowercase, uppercase and digits) of this size
    """
    alphabet = alphabet or (string.ascii_letters + string.digits)
    return ''.join(random.choice(alphabet) for x in range(length))


def random_upload(directory, filename, length=None):
    """
    Given a directory and a filename, extract the filename extension and replace the rest with
    random characters with the given length.
    Also with the three first letters of the random name create a three directory structure level.

    Example: uploadedfile.txt => a/x/j/axj091skemdywk1.txt
    Example: uploadedfile     => q/w/r/qwrwdwlwkw0122k
    """
    length = length or 15
    filename = filename.split('.')
    extension = filename[-1] if len(filename) > 1 else ''

    new_filename = random_string(length, string.ascii_lowercase + string.digits)
    if extension:
        new_filename += '.' + extension

    new_filename = '/'.join(list(new_filename[0:3])) + '/' + new_filename
    return directory + new_filename


def upload_to_random(dir_, length=None):
    """
    Wrapper function to be used as upload_to argument. Example:
    ...
    image = models.ImageField(upload_to=upload_to_random('profiles/'))
    ...
    """
    return lambda instance, filename: random_upload(dir_, filename, length)
