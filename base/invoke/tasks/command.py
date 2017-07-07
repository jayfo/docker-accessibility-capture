import subprocess
import sys


def run(command, error_on_failure=True):
    # for line in process.stdout:
    #     flag_print = line.startswith('Step ')
    #
    #     if flag_print:
    #         print(line, end='', flush=True)

    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    output = ''
    for line in process.stdout:
        line = str(line, encoding='utf-8')

        output += line
        try:
            print(
                line.encode(encoding=sys.stdout.encoding, errors='backslashreplace').decode(encoding=sys.stdout.encoding),
                end='',
                flush=True
            )
        except UnicodeDecodeError:
            pass
        except UnicodeEncodeError:
            pass

    process.wait()
    process.stdout = output
    process.stderr = process.stderr.read()
    process.failed = process.returncode != 0

    if process.failed:
        if error_on_failure:
            print(
                (
                    '========================================\n'
                    'Command failed with error code: {}\n'
                    '========================================\n'
                    'COMMAND:\n'
                    '========================================\n'
                    '{}'
                    '\n'
                    '========================================\n'
                    'STDOUT:\n'
                    '========================================\n'
                    '{}'
                    '\n'
                    '========================================\n'
                    'STDERR:\n'
                    '========================================\n'
                    '{}'
                    '\n'
                    '========================================\n'
                ).format(
                    process.returncode,
                    command,
                    process.stdout,
                    process.stderr
                ),
                file=sys.stderr, flush=True
            )

            raise subprocess.CalledProcessError(
                process.returncode,
                command
            )

    return process
