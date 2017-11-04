#  pymagic.py
#  
#  Copyright 2012 ahmed youssef <xmonader@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


from sys import argv
from ctypes import *


libmagic=None
try:
	libmagic=CDLL("libmagic.so") #or even better, check ctypes.util
except ImportError:
	print "libmagic.so is not found."
	exit(1)
	
##man libmagic

#magic_load(magic_t cookie, const char *filename);

    #Description

#These functions operate on the magic database file which is described in magic(5).

#The function magic_open() creates a magic cookie pointer and returns it. It returns NULL if there was an error allocating the magic cookie. The flags argument specifies how the other magic functions should behave:

#MAGIC_NONE'                No special handling.

    #MAGIC_DEBUG' Print debugging messages to stderr.

    #MAGIC_SYMLINK
    #If the file queried is a symlink, follow it.

    #MAGIC_COMPRESS
    #If the file is compressed, unpack it and look at the contents.

    #MAGIC_DEVICES
    #If the file is a block or character special device, then open the device and try to look in its contents.

    #MAGIC_MIME' Return a mime string, instead of a textual description.

    #MAGIC_CONTINUE
    #Return all matches, not just the first.

    #MAGIC_CHECK' Check the magic database for consistency and print warnings to stderr.

    #MAGIC_PRESERVE_ATIME
    #On systems that support utime(2) or utimes(2), attempt to preserve the access time of files analyzed.

    #MAGIC_RAW' Don't translate unprintable characters to a \ooo octal representation.

    #MAGIC_ERROR' Treat operating system errors while trying to open files and follow symlinks as real errors, instead of printing them in the magic buffer.

    #The magic_close() function closes the magic(5) database and deallocates any resources used.

    #The magic_error() function returns a textual explanation of the last error, or NULL if there was no error.

    #The magic_errno() function returns the last operating system error number ( errno(3)) that was encountered by a system call.

    #The magic_file() function returns a textual description of the contents of the filename argument, or NULL if an error occurred. If the filename is NULL, then stdin is used.

    #The magic_buffer() function returns a textual description of the contents of the buffer argument with length bytes size.

    #The magic_setflags() function, sets the flags described above.

    #The magic_check() function can be used to check the validity of entries in the colon separated database files passed in as filename, or NULL for the default database. It returns 0 on success and -1 on failure.

    #The magic_compile() function can be used to compile the the colon separated list of database files passed in as filename, or NULL for the default database. It returns 0 on success and -1 on failure. The compiled files created are named from the basename(1) of each file argument with ".mgc" appended to it.

    #The magic_load() function must be used to load the the colon separated list of database files passed in as filename, or NULL for the default database file before any magic queries can performed.

    #The default database file is named by the MAGIC environment variable. If that variable is not set, the default database file name is /usr/share/file/magic.

    #magic_load() adds ".mime" and/or ".mgc" to the database filename as appropriate.
    #Return Values

#The function magic_open() returns a magic cookie on success and NULL on failure setting errno to an appropriate value. It will set errno to EINVAL if an unsupported value for flags was given. The magic_load(), magic_compile(), and magic_check() functions return 0 on success and -1 on failure. The magic_file(), and magic_buffer() functions return a string on success and NULL on failure. The magic_error() function returns a textual description of the errors of the above functions, or NULL if there was no error. Finally, magic_setflags() returns -1 on systems that don't support utime(2), or utimes(2) when MAGIC_PRESERVE_ATIME is set. 


MAGIC_NONE=0x000000 				# No flags 
MAGIC_DEBUG=0x000001 				# Turn on debugging 
MAGIC_SYMLINK=0x000002 				# Follow symlinks 
MAGIC_COMPRESS=0x000004				# Check inside compressed files 
MAGIC_DEVICES=0x000008	 			# Look at the contents of devices 
MAGIC_MIME_TYPE=0x000010			# Return only the MIME type 
MAGIC_CONTINUE=0x000020 			# Return all matches 
MAGIC_CHECK=0x000040 				# Print warnings to stderr 
MAGIC_PRESERVE_ATIME=0x000080		# Restore access time on exit 
MAGIC_RAW=0x000100					# Don't translate unprint chars 
MAGIC_ERROR=0x000200 				# Handle ENOENT etc as real errors 
MAGIC_MIME_ENCODING=0x000400 		# Return only the MIME encoding 
MAGIC_MIME=(MAGIC_MIME_TYPE|MAGIC_MIME_ENCODING)
MAGIC_NO_CHECK_COMPRESS=0x001000 	# Don't check for compressed files 
MAGIC_NO_CHECK_TAR=0x002000 		# Don't check for tar files 
MAGIC_NO_CHECK_SOFT=0x004000 		# Don't check magic entries 
MAGIC_NO_CHECK_APPTYPE=0x008000		# Don't check application type 
MAGIC_NO_CHECK_ELF=0x010000			# Don't check for elf details 
MAGIC_NO_CHECK_ASCII=0x020000 		# Don't check for ascii files 
MAGIC_NO_CHECK_TOKENS=0x100000 		# Don't check ascii/tokens 

# Defined for backwards compatibility; do nothing 
MAGIC_NO_CHECK_FORTRAN=0x000000 	# Don't check ascii/fortran 
MAGIC_NO_CHECK_TROFF=0x000000 	    # Don't check ascii/troff 


#typedef struct magic_set *magic_t;
#magic_t magic_open(int);
#void magic_close(magic_t);

#const char *magic_file(magic_t, const char *);
#const char *magic_descriptor(magic_t, int);
#const char *magic_buffer(magic_t, const void *, size_t);

#const char *magic_error(magic_t);
#int magic_setflags(magic_t, int);

#int magic_load(magic_t, const char *);
#int magic_compile(magic_t, const char *);
#int magic_check(magic_t, const char *);
#int magic_errno(magic_t);



magic_t=c_void_p #void pointer.

magic_open=libmagic.magic_open
magic_open.restype=magic_t
magic_open.argtypes=[c_int]


magic_close=libmagic.magic_close
magic_close.restype=None
magic_close.argtypes=[magic_t]

magic_file=libmagic.magic_file
magic_file.restype=c_char_p
magic_file.argtypes=[magic_t, c_char_p]

magic_descriptor=libmagic.magic_descriptor
magic_descriptor.restype=c_char_p
magic_descriptor.argtypes=[magic_t, c_int]

magic_buffer=libmagic.magic_buffer
magic_buffer.restype=c_char_p
magic_buffer.argtypes=[magic_t, c_void_p, c_size_t]

magic_error=libmagic.magic_error
magic_error.restype=c_char_p
magic_error.argtypes=[magic_t]

magic_setflags=libmagic.magic_setflags
magic_setflags.restype=c_int
magic_setflags.argtypes=[magic_t, c_int]

magic_load=libmagic.magic_load
magic_load.restype=c_int
magic_load.argtypes=[magic_t, c_char_p]

magic_compile=libmagic.magic_compile
magic_compile.restype=c_int
magic_compile.argtypes=[magic_t, c_char_p]

magic_check=libmagic.magic_check
magic_check.restype=c_int
magic_check.argtypes=[magic_t, c_char_p]

magic_errno=libmagic.magic_errno
magic_errno.restype=c_int
magic_errno.argtypes=[magic_t]

def errcheck(result, func, args):
    err=magic_error(args[0])
    if err is None:
        return result
    raise Exception

for f in (magic_buffer, magic_check, magic_close, magic_descriptor, magic_file, magic_load):
    f.errcheck=errcheck    

def usage():
	print "pymagic.py <file>"


def guess(filepath):
	mc=magic_open(MAGIC_NONE)
	magic_load(mc, None)
	res=magic_file(mc, filepath)
	magic_close(mc)
	return res

def console_main():
	if len(argv) != 2:
		usage()
		exit(-1)
	mc=magic_open(MAGIC_NONE)
	magic_load(mc, None)
	print argv[1]+":",magic_file(mc, argv[1])
	magic_close(mc)	

if __name__=="__main__":
	console_main()

