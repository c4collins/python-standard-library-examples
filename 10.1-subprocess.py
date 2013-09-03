## 10.1 subprocess - spawning additional processes
# subprocess was designed to replace a bunch of other things, some os.fs()s, popen, popen2, commands()
# The subprocess module defines one class Popen, and a few wrappers for use with that class
# Popen's constructor takes arguments to set up the new process so it can communicate via pipes.
# It provides all the functionality of the other modules and functions it replaces, and more
# The API is consistent for all uses,and many of the overhead steps are built in instead of being handled by application code.
## Note: the API for UNIX and Windows are roughly the same, but if you run your program on Windows, these examples might not work great.
import subprocess, os, signal, time, sys, tempfile

## 10.1 Running External Commands
# To run an external command without interacting with it, like os.system() might, use call()
subprocess.call( ['ls', '-l'] )
#  command line arguments are passed as a list of strings.

# setting the shell argument to a true value causes subprocess to spawn an intermediate shell process which then runs the command.
# using an intermediate shell means that variables, glob patters, and other special shell features are computed before the command is run
subprocess.call( 'echo $HOME', shell=True )


  ## Error Handling
# The return value from call() is the exit code of the program.  The caller is repsponsible for interpreting it to detect errors
# check_call() works like call() except that the exit code is checked and if it indicates an error happened, then a CalledProcessError exception will be raised
try:
    subprocess.check_call( ['false'] )
except subprocess.CalledProcessError as err:
    print 'Error:', err

    ## Capturing Output
# The stdin/stdout channels for the process started by call() are bound to the parent's input and output
# This means the calling program cannot capture the output of the command.
# use check_output() to capture the output for later processing 
output = subprocess.check_output( ['ls', '-l'] )

print "Have %d bytes on output" % len(output)
print output

    ## Series of Commands in a Subshell - Series Power! (that a TMNT joke...)
# Messages are sent to stdout and stderr befor ethe commands exit with an error code
try:
    output = subprocess.check_output(
        'echo to stdout; echo to sterr 1>&2; exit 1',
        shell=True,
    )
except subprocess.CalledProcessError as err:
    print 'Error:', err
else:
    print "Have %d bytes in output", len(output)
    print output
print

# The message to stderr is printed, but the message to stdout is hidden.
# To prevent error messages from commands run through check_output() from being ritten to the console, set the stderr parameter to stdout

try:
    output = subprocess.check_output(
        'echo to stdout; echo to sterr 1>&2; exit 1',
        shell=True,
        stderr=subprocess.STDOUT,
    )
except subprocess.CalledProcessError as err:
    print 'Error:', err
else:
    print "Have %d bytes in output", len(output)
    print output
print    
# now stdout and stderr are merged so if the command prints an error message it's captured and not end to the console.

## 10.1.2 Working with Pipes Directly
# The functions call(), check_call(), and check_output() are wrappers around the Popen class.  
# Using Popen directly gives more control over how the command is run and how its input and output streams are processed.
# For example, by passing different arguments for stdin, stdout, and stderr, it's possible to mimic the cariations of os.popen()

    ## One-Way Communication with a Process
# To run a process and read all its output, set the stdout value to PIPE and call communicate()
print 'read:'
proc = subprocess.Popen( [ 'echo', '"to stdout"'], stdout=subprocess.PIPE, )
stdout_value = proc.communicate()[0]
print "\tstdout:", repr( stdout_value )

print 'write:'
proc = subprocess.Popen( [ 'cat', '-'], stdin=subprocess.PIPE, )
proc.communicate( "\tstdin: to stdin" )
print
    ## Bidirectional Communication with a Process
# Combine the previous two options
print 'popen2:'
proc = subprocess.Popen( ['cat', '-', ],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
)
msg = "through stdin to stdout"
stdout_value = proc.communicate(msg)[0]
print "\tpass through:", repr(stdout_value)

# It's also possible to watch stderr
print 'popen3:'
proc = subprocess.Popen( 'cat -; echo "to stderr" 1>&2',
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True,
)
msg = "through stdin to stdout"
stdout_value, stderr_value = proc.communicate(msg)
print "\tpass through:", repr(stdout_value)
print "\tstderr      :", repr(stderr_value)

# And to combine stderr and stdout
print 'popen4:'
proc = subprocess.Popen( 'cat -; echo "to stderr" 1>&2',
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    shell=True,
)
msg = "through stdin to stdout"
stdout_value, stderr_value = proc.communicate(msg)
print "\tcombined    :", repr(stdout_value)
print "\tstderr      :", repr(stderr_value)

## 10.1.3 Connecting Segments of a Pipe
# Multiple commands can be connected into a pipeline, similar to the way the UNIX shell works, by creating separate Popen instances and chaining their I/Os together
# The stdout attribute of one Popen instance is used as the stdin argument fo the next in the pipeline, instead of the constant PIPE.
# the output is read from the stdout of the final command in the pipeline.
filename = 'data/file_list.txt'

# create a file to read
with open( filename, 'w') as f:
    for item in os.listdir( os.curdir ):
        f.write(item + '\n')
        
cat = subprocess.Popen( ['cat', filename], stdout=subprocess.PIPE )
grep = subprocess.Popen( ['grep', '3'], stdout=subprocess.PIPE, stdin=cat.stdout )
cut = subprocess.Popen( ['cut', '-f', '3', '-d:'], stdout=subprocess.PIPE, stdin=grep.stdout )
end_of_pipe = cut.stdout

print "Included files:"
for line in end_of_pipe:
    print '\t', line.rstrip()
print
    
# this example reproduces:
# cat data/file_list.txt | grep 3 | cut -f 3 -d

## 10.1.4 interacting with Another Command
# All the previous examples assume a limited amount of interaction.
# The communicate() method reads all the output and waits for the child process to exit before returning.
# It is also possible tow write and read from the individual pipe handles used by the Popen instance incrementally, as the program rune.
# A simple echo program that read from the stdin and writes to stdout illustrates this technique

# 10.1.4-subprocess_repeater.py comprises the first half of this example

print "One line at a time:"
proc = subprocess.Popen( 'python 10.1.4-subprocess_repeater.py',
    shell=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
)

for i in xrange(5):
    proc.stdin.write('%d\n' % i)
    output = proc.stdout.readline()
    print output.rstrip()
remainder = proc.communicate()[0]
print remainder
print
print "All output at once:"
proc = subprocess.Popen( 'python 10.1.4-subprocess_repeater.py',
    shell=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
)

for i in xrange(5):
    proc.stdin.write('%d\n' % i)
output = proc.communicate()[0]
print output
time.sleep(3)
print

## 10.1.5 Signalling Between Processes
# The process management examples for the os module include a demo of signalling between processes using os.fork() and os.kill()
# Since each Popen instance provides a pid attribute with the process id of the child process, it is possible to do something similar with subprocess
# The next example combines two scripts.

# 10.1.5-subprocess_signal-child.py comprises the first half of this example

proc = subprocess.Popen( ['python', '10.1.5-subprocess_signal-child.py'] )
print "PARENT       : Pausing before sending signal..."
sys.stdout.flush()
time.sleep(1)
print "PARENT       : Signalling child"
sys.stdout.flush()
os.kill( proc.pid, signal.SIGUSR1 )
time.sleep(2)
print

  ## Process Groups / Sessions
# if the process created by Popen spawns subprocesses, those children will not receive any signals sent to the parent.
# This means that when using the shell argument to Popen it will be difficult to cause the command started in the shell to terminate by sending SIGINT or SIGTERM
script = '''#!/bin/sh
echo "Shell script in process $$"
set -x
python 10.1.5-subprocess_signal-child.py
'''
script_file = tempfile.NamedTemporaryFile('wt')
script_file.write(script)
script_file.flush()

proc = subprocess.Popen( [ 'sh', script_file.name ], close_fds=True)
print "PARENT       : Pausing before sending signal %s..." % proc.pid
sys.stdout.flush()
time.sleep(1)
print "PARENT       : Signalling child %s" % proc.pid
sys.stdout.flush()
os.kill( proc.pid, signal.SIGUSR1 )
time.sleep(1)
print

# This happens because the pid used to send the signal doesn't match the pid of the child of the shell script waiting for the signal.  Parent -> Shell -> Child
# To send signals to descendants without knowing their process id, use a process proup to associate the childre so they can be signaled together.
# The process group is created with os.setsid(), setting the "session id" to the process id of the current process.
# All child processes inherit their session id from their parent, and since it should only be set in the shell created by Popen and it's descendants,
# os.setsid() shoudl not be caled in the same process where Popen is created.  Instead the function is passed to Popen as the preexec_fn argument,
# so it is run after the fork() inside the new process, before it used exec() to run the shell.
# To signal the entire process group, us os.killpg() with the pid value from the Popen instance.

def show_setting_sid():
    print 'Calling os.setsid() from %s' % os.getpid()
    sys.stdout.flush()
    os.setsid()
    
proc = subprocess.Popen( [ 'sh', script_file.name ], close_fds=True, preexec_fn=show_setting_sid)
print "PARENT       : Pausing before sending signal %s..." % proc.pid
sys.stdout.flush()
time.sleep(1)
print "PARENT       : Signalling child %s" % proc.pid
sys.stdout.flush()
os.killpg( proc.pid, signal.SIGUSR1 )
time.sleep(1)
print

# 1. Parent program instantiates Popen
# 2. Popen forks a new process
# 3. new process runs os.setsid()
# 4. new process runs exec() to start the shell
# 5. the shell runs the shell script
# 6. the shell forks again, and that process execs Python
# 7. Python runs 10.1.5-subprocess_signal-child.py
# 8. Parent program signals the process group using the pid of the shell
# 9. Shell and Python process receive he signal
# 10. Shell ignores the signal
# 11. Python invokes the signal handler