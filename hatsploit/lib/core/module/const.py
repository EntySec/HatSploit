"""
MIT License

Copyright (c) 2020-2024 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

SIDE_EFFECTS = 1000

"""
Side Effects
"""

ARTIFACTS_ON_DISK = SIDE_EFFECTS + 1
IOC_IN_LOGS = SIDE_EFFECTS + 2

STABILITY = 2000

"""
Stability
"""

CRASH_SAFE = STABILITY + 1
CRASH_DOWN = STABILITY + 2
ACCOUNT_LOCKOUTS = STABILITY + 3

RELIABILITY = 3000

"""
Reliability
"""

RELIABLE_SESSION = RELIABILITY + 1
WEAK_SESSION = RELIABILITY + 2

HIGH_RANK = "high"
MEDIUM_RANK = "medium"
LOW_RANK = "low"
