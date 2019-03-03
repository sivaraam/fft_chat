# A test python 3 program that:
#
#    1. Takes text as input
#    3. Applies FFT to the the text (in it's corresponding numerical value)
#    4. Prints the output of FFT
#    5. Applies inverse FFT to the FFT output
#    6. Converts it back to text
#    7. Prints the resulting text
#

import numpy as np
# import base64

def process(utf8_string_in):
    """
    The intermediary base64 conversion seems to be having issues such as
    "incorrect padding" when decoding, etc.

    Further the reason why this intermediary conversion was done
    (to successfully send UTF-8 strings), tuned out to work even without
    this conversion. So, skip it for now.
    """
#    base64_encoded_out = base64.b64encode(bytes(utf8_string_in, "utf-8"))
#    print("Base64 encoded string: ", base64_encoded_out)

    """
    Create an array whose elements are Unicode code points (number)
    for each character in the given string.
    """
    fft_array_in = [ord(char) for char in utf8_string_in]

    """
    Apply FFT to the array
    """
    fft_array_out = np.fft.fft(fft_array_in)
    print("After applying FFT: ", fft_array_out)

    """
    Apply inverse FFT to the array
    """
    ifft_array_out = np.fft.ifft(fft_array_out)
    print("After applying inverse FFT: ", ifft_array_out)

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

    """
    See note near base64.b64encode code
    """
#    base64_decoded_out = base64.b64decode(bytes(ascii_string_in, "ascii"))
#    print("After Base64 decode: ", base64_decoded_out)

    return utf8_string_out

while True:
    utf8_string_in = input('Enter a message: ')
    print("String input: ", utf8_string_in)
    utf8_string_out = process(utf8_string_in)
    print("String output: ", utf8_string_out)
    print()
