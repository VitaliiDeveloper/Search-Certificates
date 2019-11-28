import os
import argparse
import subprocess
import shutil

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str)
    parser.add_argument("--teamId", type=str)
    parser.add_argument("--bundleId", type=str)
    parser.add_argument("--password", type=str)

    args = parser.parse_args()

    listOfFiles = []
    for path, subdir, files in os.walk(args.path):
        for file in files:
            if file.find(".p12") != -1:
                listOfFiles.append(path + "/" + file)


    availableFiles = []
    for cert in listOfFiles:
        try:
            passPassword = "%s%s" % ("pass:", args.password)
            cert_bytes = subprocess.check_output(["openssl", "pkcs12", "-in", cert, "-info",
                                                  "-passin", passPassword, "-passout", passPassword])
            cert_txt = cert_bytes.decode("utf-8")

            cert_txt_args = ""
            if not args.teamId:
                cert_txt_args = "%s/OU=%s" % (args.bundleId, args.teamId)
            else:
                cert_txt_args = args.bundleId

            if cert_txt_args in cert_txt:
                availableFiles.append(cert)
        except subprocess.CalledProcessError as error:
            print("ERROR Subprocess: %s" % error)

    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'Certificates')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    for cert in availableFiles:
        shutil.copy(cert, final_directory, follow_symlinks=False)


if __name__ == "__main__":
    main()
