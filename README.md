# regalter-utility

Regalter: A simple utility for changing the registered owner and registered organization names without messing with Windows registry.

## Possible uses of Regalter
The recent releases of Windows 10 does not allow the user to enter the user and organization names during installation. Instead it
asks the user to sign in with his/her Microsoft account. The user and organization names are extracted from the user's Microsoft
account information. However, if the user skips signing in to his/her Microsoft account then the organization name is not written
to the Windows Registry. That is when you need a simple tool like Regalter. Again, when the user wishes to transfer his/her Windows
PC's ownership to someone else and he/she wishes to change the registered owner and organization names, Regalter makes the work easy
for the user.

## Description
There are two versions of the source files, 64-bit and 32-bit. The 32-bit source files are in the directory named `x86`. The
existence of different source files (almost similar though) for 32-bit and 64-bit versions of Regalter is due to the different architectures
of Windows Registry for 32-bit and 64-bit Windows. To learn more about 32-bit and 64-bit Registry, refer to the links below:

* https://docs.microsoft.com/en-us/windows/win32/sysinfo/32-bit-and-64-bit-application-data-in-the-registry

* https://docs.microsoft.com/en-us/troubleshoot/windows-client/deployment/view-system-registry-with-64-bit-windows

* https://stackoverflow.com/questions/869783/windows-64-bit-registry-v-s-32-bit-registry

The 64-bit version of Regalter (**exclusively for 64-bit Windows**) has been designed to look for the values of `RegisteredOwner`
and `RegisteredOrganization` at two locations in the Windows 64-bit Registry, i.e., under `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\`
(which is accessible to 64-bit programs only) and under `HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\` (which is accessible
to both 64-bit and 32-bit programs). The former location is inaccessible to 32-bit programs and hence the values at the latter location also
need to be modified. This is, however, not the case with the 32-bit version of Regalter (**which has been exclusively designed to run on
32-bit Windows**) and values of `RegisteredOwner` and `RegisteredOrganization` are searched and modified only under `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\`.
Note that the 32-bit version of Regalter may be able to run on 64-bit Windows, but will fail to modify the values under `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\`
and will only be able to modify the values under `HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\`, since the former location is
not accessible to 32-bit applications on 64-bit Windows. Hence, it is recommended to check your Windows architecture before using either the
32-bit or 64-bit version of Regalter and make sure that the architectures of Windows and Regalter match to get the correct results.

## System requirements
* 100 MB of free disk space, and other usual hardware requirements any software has;
* Windows XP (Service Pack 3) or newer Windows operating system;
* Microsoft Visual C++ 2010, 2013, 2015-19 redistributable.

## Copyright notice
Here is the notice which has been included with all the source code files:
```
Copyright (C) 2021 Arijit Kumar Das (Github: @ArijitKD)

Regalter is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Regalter is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```

## Contact
For any suggestions or for reporting bugs, please send an e-mail to arijitkdgit.official@gmail.com.
