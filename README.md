# Extended-kmp
A space and time efficient pattern matching algorithm that finds all the exact occurrences of pattern in text.

## Inputs
1. An input file containing txt[1..n] (without any line breaks)
2. Another input file containing pat[1..m] (without any line breaks)

## Output
Output file name: output_kmp.txt

The program will output each position where pat matches the txt in a seperate line.

## Run the script in command line
extended_kmp.py <text_file> <pattern_file>

## Example 
text = abcdabcdabcd, pattern = abc

### Output: 
1 <br>
5 <br>
9 
