from scapy.all import *
import re
import os


def extract_images(pcap_file, output_dir="extracted_images"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    packets = rdpcap(pcap_file)
    sessions = packets.sessions()
    count = 0

    for session in sessions:
        payload = b""
        for packet in sessions[session]:
            if packet.haslayer(Raw):
                payload += bytes(packet[Raw].load)

        # Image signatures to look for
        signatures = {
            b"\x89PNG\r\n\x1a\n": (b"IEND", "png"),         # PNG
            b"GIF89a": (b"\x00\x3B", "gif"),               # GIF89a
            b"GIF87a": (b"\x00\x3B", "gif"),               # GIF87a
            # JPEG/JFIF start to end
            b"\xff\xd8\xff": (b"\xff\xd9", "jpg"),
        }

        for sig, (end_marker, ext) in signatures.items():
            search_from = 0
            while True:
                start = payload.find(sig, search_from)
                if start == -1:
                    break
                end = payload.find(end_marker, start)
                if end == -1:
                    break
                if ext == "jpg":
                    end += 2
                elif ext == "png":
                    end += 4
                elif ext == "gif":
                    end += 2

                image_data = payload[start:end]
                file_path = os.path.join(
                    output_dir, f"extracted_{count}.{ext}")
                with open(file_path, "wb") as f:
                    f.write(image_data)
                count += 1
                search_from = end

    print(f"Extraction complete. {count} image(s) saved to '{output_dir}'.")


# Example usage
extract_images("location.pcapng")
