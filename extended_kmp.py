"""
name: Johan Azlan
student ID: 31165001

"""
import sys


"""
A function used to read the two text files. One of the input file contains the text and the other contains the pattern.

"""
def readInput(txtFileName, patFileName):
    # Open and read the txt file
    txtFile = open(txtFileName, 'r')
    txt = txtFile.read()

    # Close the file
    txtFile.close()

    # Open and read the pattern file
    patFile = open(patFileName, 'r')
    pat = patFile.read()

    # Close the file
    patFile.close()

    # Return the pattern and text
    return txt, pat


"""
A function used to write the output of extended_kmp() to the output file output_kmp.txt. Each position where pat matches txt will be in a seperate line.   

"""
def writeOutput(occurrences):
    # Open output file with correct name 
    outputFile = open("output_kmp.txt", "w")

    if occurrences == []:
        outputFile.write("")
    
    else:
        # Iterate through the occurrence list and write results to an output file
        outputFile.write(str(occurrences[0] + 1))
        for i in range(1, len(occurrences)):
            outputFile.write('\n')
            outputFile.write(str(occurrences[i] + 1))

    # Close the file
    outputFile.close()


"""
z algo for prefixes

"""
def zalgo(pat):
    z = [None] * len(pat) 
    z[0] = len(pat) # first position is the length of pat

    # variables 
    l, r = 0, 0
    matches = 0
    i = 1 

    for i in range(1, len(pat)):
        
        # Case 1: i is outside the box
        if i > r:
            pointer = i
            j = 0
            matches = 0

            # compare outside box, matches += 1 each time character match
            while pointer < len(pat) and pat[j] == pat[pointer]:
                j += 1
                pointer += 1
                matches += 1
        
            # Form the z-box
            if matches > 0:
                z[i] = matches
                l = i
                r = i + matches - 1
            
            else: 
                z[i] = 0

        # Case 2a, 2b, 2c: i is inside the box
        else: 
            k = i - l # index of prefix which corresponds to the index of substring that matches
            remaining = r - i + 1

            # case 2a: z[k] < remaining
            if z[k] < remaining:
                z[i] = z[k]

            # case 2b: z[k] > remaining
            elif z[k] > remaining:
                z[i] = remaining
            
            # case 2c: z[k] == remaining
            elif z[k] == remaining:
                matches = remaining 

                # compare outside box, matches += 1 each time character match
                pointer1 = r - i + 1  
                pointer2 = r + 1
                
                while pointer2 < len(pat) and pat[pointer1] == pat[pointer2]:
                    matches += 1
                    pointer1 += 1
                    pointer2 += 1

                # Form the z-box
                z[i] = matches
                l = i 
                r = i + matches - 1

    return z


"""
An algorithm which implements the KMP algorithm with modifications in the shifting rule to make it more strict. Finds all the exact occurrences of pat in txt. 

"""
def extended_kmp(txt, pat):

    # if txt or pat or both are empty, return empty list
    if txt == "" or pat == "":
        return []

    else:

        # preprocessing
        z_array = zalgo(pat)
        sp = [0] * len(pat)
        m = len(sp) - 1

        # pointers

        # These 2 pointers will change their start and end point when a shift occurs 
        pat_start = 0          
        pat_end = len(pat)-1

        # This pointer is used for comparing characters in pat with txt
        pat_pointer = 0 

        # This pointer is used for comparing characters in txt with pat
        txt_pointer = 0

        shift = 0
        match = True
        matched_length = 0
        result = []    

        # Fill in SP_i array 
        for j in range(m, 0, -1): # Loops from char at index m down to char at index 1 
            i = j + z_array[j] - 1
            sp[i] = z_array[j]


        while pat_end + shift <= len(txt) - 1:
            
            # Updated variables for the next iteration 
            pat_start += shift 
            pat_end += shift
            match = True

            # Galil's optimisation 
            # Skip comparison of txt and pat before index of txt_pointer + 1. Only compare characters starting from index of txt_pointer + 1
            if shift < pat_pointer: 
                matched_length = txt_pointer - pat_start + 1 # txt_pointer - pat_start + 1 is the region in pat that matches with txt after shift 
                pat_pointer = txt_pointer - pat_start + 1 # pat_start has already been updated with the shift. txt_pointer - pat_start + 1 is the starting point for comparison.
                txt_pointer = txt_pointer + 1 # txt_pointer begins from txt_pointer + 1 because the prefix has aligned to match txt from 1..SP[i]. Need to start comparing from txt_pointer + 1 as txt_pointer was the index of mismatch in txt

            # if shift > pat_pointer, it means that there wont be a region in pat that is already matched as the whole pat needs to be compared again
            else:
                pat_pointer = 0 # Reset the pat_pointer to 0
                txt_pointer = pat_start # txt_pointer will be equal to pat_start which is the start position after shift
                matched_length = 0 # matched_length reset to 0


            while pat_pointer < len(pat) and match == True: # Needs to be < than the last char index because the mismatch will occur at pat_pointer + 1
                
                # Compare characters in pat and txt. if they are the same then increment the pointers and matched length
                if pat[pat_pointer] == txt[txt_pointer]:
                    pat_pointer += 1
                    txt_pointer += 1
                    matched_length += 1

                #! Check for full match between txt and pat once it completes the inner while loop 
                    if matched_length == len(pat):
                        shift = len(pat) - sp[m-1] # shift by the length of pat as it is already a full match
                        result.append(pat_start) # Append the starting point index of pat which has a full match with txt

                # mismatch happens at position i ; need to look at sp[i-1]
                elif pat[pat_pointer] != txt[txt_pointer]:
                    match = False # This is used to exit the loop 

                    # Check if there exists a longest proper suffix 
                    if pat[pat_pointer] != 0: 
                        if sp[pat_pointer - 1] > 0:
                            
                            # if exists, Check if pat[prefix + 1] == txt[txt_pointer]
                            prefix = sp[pat_pointer - 1] - 1 # index of the right endpoint of the prefix 

                            if pat[prefix + 1] == txt[txt_pointer]: # it is not txt_pointer + 1 because mismatch happens at position txt_pointer 
                            
                                # shift only if we know that pat[prefix + 1] == txt[txt_pointer]
                                shift = pat_pointer - sp[pat_pointer - 1]

                        # If SP[i-1] value is 0, shift pat to position mismatch + 1
                        else:
                            shift = pat_pointer + 1

        return result


if __name__ == "__main__":
    # First retrieve the file names from the console
    txtFileName = sys.argv[1]
    patFileName = sys.argv[2]

    # Read in the text and pattern from these files
    txt, pat = readInput(txtFileName, patFileName)

    # Process the text and pattern 
    occurrences = extended_kmp(txt, pat) # occurrences is a list of tuples 

    # Write your output to a correctly named file
    writeOutput(occurrences)
