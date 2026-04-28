# ╔══════════════════════════════════════════════════════════════╗
# ║  JARVIS MODULE 2: SYSTEM UTILITIES (THE SILENCER)            ║
# ║  Focus: Suppressing Terminal Noise (ALSA/JACK Errors)        ║
# ╚══════════════════════════════════════════════════════════════╝

import os
import sys
from contextlib import contextmanager

# ================================================================
# FUNCTION: suppress_alsa_errors (The Silencer)
# ================================================================

@contextmanager
def suppress_alsa_errors():
    """
    KAAM: Terminal par aane wale ALSA/JACK ke faltu errors ko chhupana.
    KYUN: Taki jab mic start ho, toh terminal saaf dikhe aur sirf kaam ki baat ho.
    RETURN: Context Manager (Use with 'with' block).
    """
    
    # 1. '/dev/null' ek aisi jagah hai jahan jo bhi data jayega wo gayab ho jayega.
    # OS level par ise open kar rahe hain.
    devnull = os.open(os.devnull, os.O_WRONLY)
    
    # 2. File Descriptor 2 (Standard Error) ka ek backup le rahe hain.
    # Taki baad mein ise restore kar sakein.
    old_stderr = os.dup(2)
    
    # 3. Python ke stderr buffer ko flush kar rahe hain taaki koi pending error na bache.
    sys.stderr.flush()
    
    # 4. Asli Magic: Standard Error (FD 2) ko redirect kar rahe hain '/dev/null' ki taraf.
    # Ab Linux audio libraries jo bhi errors phenkengi, wo seedha /dev/null mein jayengi.
    os.dup2(devnull, 2)
    os.close(devnull)
    
    try:
        # Yahan par execution wapas 'with' block ke andar chali jayegi.
        yield
    finally:
        # 5. Restore: Jab kaam khatam ho jaye, toh FD 2 ko wapas purane raste par dal do.
        os.dup2(old_stderr, 2)
        os.close(old_stderr)

# ================================================================
# JARVIS TIP: 
# Ise use karne ke liye module1.py ya practice.py mein import karein:
# from module2 import suppress_alsa_errors
# 
# Phir 'with suppress_alsa_errors():' ke andar mic wala code likhein.
# ================================================================
