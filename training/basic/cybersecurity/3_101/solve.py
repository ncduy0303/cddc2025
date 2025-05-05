with open("this_is_yours.txt", "r") as f:
    line = f.readline()
    # Split the line into binary numbers
    binaries = line.strip().split()
    # Convert each binary string to a char using ASCII
    text = ''.join([chr(int(b, 2)) for b in binaries])
    flag = text.split("CDDC2025{")[1].split("}")[0]
    # Print the flag
    print(f"CDDC2025{{{flag}}}")