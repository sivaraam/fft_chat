# A library that provides 2 APIs for the FFT
# chat application for the sending part and
# receiving part.
#

import numpy as np
# import base64
import pickle

"""
Function fft_send:

Accepts a message as an argument.

Description:
1. Takes text as input
2. Applies FFT to the the text (in
   it's corresponding numerical value)
3. Returns the serialized bytes of the FFT array

"""
def fft_send(utf8_string_in):
    """
    Create an array whose elements are Unicode code points (number)
    for each character in the given string.
    """
    fft_array_in = [ord(char) for char in utf8_string_in]

    """
    Apply FFT to the array
    """
    fft_array_out = np.fft.fft(fft_array_in)

    return pickle.dumps(fft_array_out)

"""
Function fft_receive:

Accepts the serialized FFT bytes as the argument

1. De-serializes the output
2. Applies inverse FFT to the de-serialized FFT output
3. Converts it back to text

"""
def fft_receive(serialized_fft_bytes):
    deserialized_fft_array = pickle.loads(serialized_fft_bytes)

    """
    Apply inverse FFT to the array
    """
    ifft_array_out = np.fft.ifft(deserialized_fft_array)

    """
    Create an array of utf8 chars from the obtained inverse FFT
    output.

    Note:
    * The output of inverse FFT is a array of complex values

    * abs(ifft_char): In most cases applying FFT and immediately applying
                      inverse FFT shouldn't have a imaginary component.
                      We take abs() just in case.

    * round(abs): This is required as the float value after taking inverse FFT
                  is not "precisely" the value given as input. i.e., if 10.0 is
                  input the corresponding output may be 9.99999999...

                  We use round() to get the correct value.

    * int(round): chr() takes integer as an argument. So, we convert to integer.

    * chr(int): To get the Unicode string for the given ordinal value
    """
    utf8_chars_array_out = [chr(int(round(abs(ifft_char)))) for ifft_char in ifft_array_out]

    """
    Merge the characters into a string
    """
    utf8_string_out = "".join(utf8_chars_array_out)

    return utf8_string_out
