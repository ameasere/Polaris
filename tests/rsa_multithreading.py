import rsa
import multiprocessing
import psutil
import colorama
import time
import sys

t1_header = "[T1] "
t2_header = "[T2] "

colorama.init()  # Initialize Colorama for colored output


def generate_color_bar(progress):
    # Define the RGB values for white and teal blue
    purple_rgb = (85, 207, 237)
    teal_blue_rgb = (158, 119, 237)

    # Calculate the number of boxes to display based on progress
    num_boxes = int(progress * 30)

    # Interpolate the color based on the progress
    interpolated_color = (
        int(purple_rgb[0] + progress * (teal_blue_rgb[0] - purple_rgb[0])),
        int(purple_rgb[1] + progress * (teal_blue_rgb[1] - purple_rgb[1])),
        int(purple_rgb[2] + progress * (teal_blue_rgb[2] - purple_rgb[2]))
    )

    # Convert RGB values to Colorama color format and create the colored boxes
    color = f"\033[38;2;{interpolated_color[0]};{interpolated_color[1]};{interpolated_color[2]}m"
    colored_boxes = "▓" * num_boxes
    empty_boxes = " " * (30 - num_boxes)

    return color + colored_boxes + '\033[0m' + empty_boxes


def update_progress(progress, label):
    bar = generate_color_bar(progress)
    sys.stdout.write(
        '\r{} progress: ║{}║ {:.2f}%'.format(
            label, bar, progress * 100))
    sys.stdout.flush()


def main_thread():
    print(
        colorama.Fore.GREEN +
        t1_header +
        "Main thread started" +
        colorama.Style.RESET_ALL)
    start = time.time()
    (public_key, private_key) = rsa.newkeys(2048, poolsize=int(
        psutil.cpu_count()) - 2 if psutil.cpu_count() > 2 else 1)
    end = time.time()
    # print(colorama.Fore.BLUE + t1_header + "Public key: " + colorama.Style.RESET_ALL + str(public_key))
    # print(colorama.Fore.BLUE + t1_header + "Private key: " + colorama.Style.RESET_ALL + str(private_key))
    print(colorama.Fore.RED + t1_header + "Time taken to generate keys: " +
          colorama.Style.RESET_ALL + str(round(end - start, 2)) + " seconds")
    # Encrypt a string then decrypt it
    message = "Hello World!"
    start_2 = time.time()
    encrypted_message = rsa.encrypt(message.encode(), public_key)
    end_2 = time.time()
    # print(colorama.Fore.BLUE + t1_header + "Encrypted message: " + colorama.Style.RESET_ALL + str(encrypted_message))
    print(colorama.Fore.RED + t1_header + "Time taken to encrypt: " + \
          colorama.Style.RESET_ALL + str(round(end_2 - start_2, 2)) + " seconds")
    start_3 = time.time()
    decrypted_message = rsa.decrypt(encrypted_message, private_key)
    end_3 = time.time()
    # print(colorama.Fore.BLUE + t1_header + "Decrypted message: " + colorama.Style.RESET_ALL + str(decrypted_message))
    print(colorama.Fore.RED + t1_header + "Time taken to decrypt: " + \
          colorama.Style.RESET_ALL + str(round(end_3 - start_3, 2)) + " seconds")
    print(
        colorama.Fore.GREEN +
        t1_header +
        "Main thread ended" +
        colorama.Style.RESET_ALL)


def secondary_thread():
    print(
        colorama.Fore.GREEN +
        t2_header +
        "Secondary thread started" +
        colorama.Style.RESET_ALL)
    start = time.time()
    (public_key, private_key) = rsa.newkeys(2048, poolsize=int(
        psutil.cpu_count()) - 2 if psutil.cpu_count() > 2 else 1)
    end = time.time()
    # print(colorama.Fore.BLUE + t2_header + "Public key: " + colorama.Style.RESET_ALL + str(public_key))
    # print(colorama.Fore.BLUE + t2_header + "Private key: " + colorama.Style.RESET_ALL + str(private_key))
    print(colorama.Fore.RED + t2_header + "Time taken to generate keys: " +
          colorama.Style.RESET_ALL + str(round(end - start, 2)) + " seconds")
    # Encrypt a much longer string then decrypt it
    message = "Hello World! " * 2000
    encrypted_message = b''
    decrypted_message = b''
    start_2 = time.time()
    for i in range(0, len(message), round((int(2048 / 8) - 11))):
        chunk = message[i:i + round((int(2048 / 8) - 11))]
        encrypted_message += rsa.encrypt(chunk.encode(), public_key)
        # Print progress
        update_progress(i / len(message), "[T2] Encryption")
        # Delay
        time.sleep(0.01)
    # If the progress bar doesn't say 100%, then flush the system output and print the 100% bar
    # Only if "i" exists and is not undefined
    if 'i' in locals():
        if i / len(message) != 1:
            sys.stdout.flush()
            update_progress(1, "[T2] Encryption")
    else:
        sys.stdout.flush()
        update_progress(1, "[T2] Encryption")
    print()
    end_2 = time.time()
    # print(colorama.Fore.BLUE + t2_header + "Encrypted message: " + colorama.Style.RESET_ALL + str(encrypted_message))
    print(colorama.Fore.RED + t2_header + "Time taken to encrypt: " + \
          colorama.Style.RESET_ALL + str(round(end_2 - start_2, 2)) + " seconds")
    start_3 = time.time()
    for i in range(0, len(encrypted_message), int(2048 / 8)):
        chunk = encrypted_message[i:i + int(2048 / 8)]
        decrypted_message += rsa.decrypt(chunk, private_key)
        # Print progress
        update_progress(i / len(encrypted_message), "[T2] Decryption")
        # Delay
        time.sleep(0.05)
    # If the progress bar doesn't say 100%, then flush the system output and
    # print the 100% bar
    if i / len(encrypted_message) != 1:
        sys.stdout.flush()
        update_progress(1, "[T2] Decryption")
    print()
    end_3 = time.time()
    # print(colorama.Fore.BLUE + t2_header + "Decrypted message: " + colorama.Style.RESET_ALL + str(decrypted_message))
    print(colorama.Fore.RED + t2_header + "Time taken to decrypt: " + \
          colorama.Style.RESET_ALL + str(round(end_3 - start_3, 2)) + " seconds")
    print(
        colorama.Fore.GREEN +
        t2_header +
        "Secondary thread ended" +
        colorama.Style.RESET_ALL)


if __name__ == "__main__":
    # main_process = multiprocessing.Process(target=main_thread)
    secondary_process = multiprocessing.Process(target=secondary_thread)

    # main_process.start()
    secondary_process.start()

    # main_process.join()
    secondary_process.join()

# Use RSA-chunking + multiprocessing for encryption and decryption.
# More found in my repository: https://github.com/ameasere/EasyRSA
