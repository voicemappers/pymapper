import subprocess
import sys
import threading

LOG_FILE = sys.stderr

RECORD_COMMAND = 'arecord -f cd -r 16 -c 1 -d %s > %s'
SPHINX_EXEC_SUFFIX = '/src/programs/pocketsphinx_continuous'
SPHINX_HMM = '/model/en-us/en-us'
SPHINX_ALL_PHONE = '/model/en-us/en-us-phone.lm.bin'  # give invalid for untrained

record_semaphore = threading.Semaphore(1)


def execute_sphinx_command(root_dir, infile, outfile):
    out_handle = open(outfile, "w")
    err_handle = open("err" + outfile, "w")
    result = subprocess.call(
        [
            "%s -hmm %s -allphone %s -backtrace yes -beam 1e-20 -pbeam 1e-20 -lw 2.0 -infile %s" \
            % (root_dir + SPHINX_EXEC_SUFFIX, root_dir + SPHINX_HMM, root_dir + SPHINX_ALL_PHONE, infile)
        ],
        stdout=out_handle,
        stderr=err_handle,
        shell=True
    )
    out_handle.close()
    return result


def execute_record_command(duration, outfile):
    return subprocess.call([RECORD_COMMAND % (duration, outfile)], shell=True, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)


def record_and_syllabalise(pocketsphinx_dir, duration, seq_no):
    record_name = "rec" + str(seq_no)
    syllable_out_name = "out" + str(seq_no)
    execute_record_command(duration, record_name)
    # print("Executed recording for", seq_no, "and got return code", execute_record_command(duration, record_name),
    #       file=LOG_FILE)
    record_semaphore.release()
    execute_sphinx_command(pocketsphinx_dir, record_name, syllable_out_name)
    # print("Executed syllable detection for", seq_no, "and got return code",
    #       execute_sphinx_command(pocketsphinx_dir, record_name, syllable_out_name), file=LOG_FILE)


def main():
    duration = input("Please enter duration in seconds: ")
    times = int(input("Please enter number of samples"))
    pocketsphinx_dir = input("Please enter the pocketsphinx directory: ")
    seq_no = 1
    threads = []
    for _ in range(times):
        record_semaphore.acquire()
        print("Start speaking")
        threads.append(threading.Thread(target=record_and_syllabalise, args=(pocketsphinx_dir, duration, seq_no)))
        threads[-1].start()
        seq_no += 1
    print("Waiting for threads!")
    for thread in threads:
        thread.join()
    print("Finished waiting on threads!")


main()
