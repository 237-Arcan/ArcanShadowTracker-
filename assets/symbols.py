"""
Symbol utilities for the ArcanShadow system.
Provides esoteric symbols and visualizations in SVG format.
"""

def get_symbol(symbol_name):
    """
    Returns an SVG representation of the requested esoteric symbol.
    
    Args:
        symbol_name (str): Name of the symbol to retrieve
            
    Returns:
        str: SVG code for the requested symbol
    """
    symbols = {
        'pentagram': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="gold" stroke-width="1.5">
                <path d="M12 2L14.4 8.5H21.5L15.8 12.9L18.2 19.5L12 15.6L5.8 19.5L8.2 12.9L2.5 8.5H9.6L12 2Z" />
            </svg>
        """,
        'moon': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="silver" stroke-width="1.5">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
            </svg>
        """,
        'sun': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="gold" stroke-width="1.5">
                <circle cx="12" cy="12" r="5"></circle>
                <line x1="12" y1="1" x2="12" y2="3"></line>
                <line x1="12" y1="21" x2="12" y2="23"></line>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                <line x1="1" y1="12" x2="3" y2="12"></line>
                <line x1="21" y1="12" x2="23" y2="12"></line>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
            </svg>
        """,
        'star': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="gold" stroke-width="1.5">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
            </svg>
        """,
        'crystal': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#9c27b0" stroke-width="1.5">
                <path d="M12 2L5 6L5 18L12 22L19 18L19 6L12 2Z" />
                <path d="M12 2L12 22" />
                <path d="M5 6L19 6" />
                <path d="M5 18L19 18" />
            </svg>
        """,
        'planet': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#4169e1" stroke-width="1.5">
                <circle cx="12" cy="12" r="7"></circle>
                <circle cx="12" cy="12" r="10" stroke-dasharray="1,3"></circle>
                <circle cx="18" cy="8" r="1"></circle>
            </svg>
        """,
        'zodiac': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="gold" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M12 2L12 12L17 17" />
            </svg>
        """,
        'tarot': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#9c27b0" stroke-width="1.5">
                <rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect>
                <circle cx="12" cy="8" r="3"></circle>
                <path d="M12 11L12 18"></path>
                <path d="M9 15L15 15"></path>
            </svg>
        """,
        'eye': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="gold" stroke-width="1.5">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
            </svg>
        """,
        'triquetra': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#9c27b0" stroke-width="1.5">
                <path d="M12 2C6.5 2 2 6.5 2 12C2 17.5 6.5 22 12 22C17.5 22 22 17.5 22 12" />
                <path d="M12 2C17.5 2 22 6.5 22 12C22 17.5 17.5 22 12 22C6.5 22 2 17.5 2 12" />
                <path d="M12 2C17.5 2 22 6.5 22 12C17.5 12 12 17.5 12 22C12 17.5 6.5 12 2 12" />
            </svg>
        """,
        'mercury': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="silver" stroke-width="1.5">
                <circle cx="12" cy="12" r="5"></circle>
                <path d="M12 17L12 22"></path>
                <path d="M9 20L15 20"></path>
                <path d="M12 7L12 2"></path>
                <circle cx="12" cy="4" r="2" stroke="none" fill="silver"></circle>
            </svg>
        """,
        'saturn': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#4169e1" stroke-width="1.5">
                <circle cx="12" cy="12" r="5"></circle>
                <path d="M12 7L12 2"></path>
                <path d="M7 20L17 20"></path>
            </svg>
        """,
        'jupiter': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#4169e1" stroke-width="1.5">
                <path d="M12 22L12 2"></path>
                <path d="M17 7L7 7"></path>
                <path d="M7 12L17 12"></path>
            </svg>
        """,
        'hexagram': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="gold" stroke-width="1.5">
                <polygon points="12 2 14.5 9 22 9 16 14 18.5 21 12 17 5.5 21 8 14 2 9 9.5 9" />
            </svg>
        """,
        'yin_yang': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="1.5">
                <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z"></path>
                <path d="M12 2C14.6522 2 17.1957 3.05357 19.0711 4.92893C20.9464 6.8043 22 9.34784 22 12C22 14.6522 20.9464 17.1957 19.0711 19.0711C17.1957 20.9464 14.6522 22 12 22"></path>
                <path d="M12 2C9.34784 2 6.8043 3.05357 4.92893 4.92893C3.05357 6.8043 2 9.34784 2 12C2 14.6522 3.05357 17.1957 4.92893 19.0711C6.8043 20.9464 9.34784 22 12 22"></path>
                <circle cx="12" cy="7" r="2" fill="#ffffff" stroke="none"></circle>
                <circle cx="12" cy="17" r="2" fill="none"></circle>
            </svg>
        """,
        'kabbalah': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#9c27b0" stroke-width="1.5">
                <circle cx="12" cy="3" r="1"></circle>
                <circle cx="6" cy="7" r="1"></circle>
                <circle cx="18" cy="7" r="1"></circle>
                <circle cx="12" cy="11" r="1"></circle>
                <circle cx="8" cy="15" r="1"></circle>
                <circle cx="16" cy="15" r="1"></circle>
                <circle cx="10" cy="19" r="1"></circle>
                <circle cx="14" cy="19" r="1"></circle>
                <path d="M12 3L6 7L8 15L10 19"></path>
                <path d="M12 3L18 7L16 15L14 19"></path>
                <path d="M6 7L12 11L18 7"></path>
                <path d="M8 15L12 11L16 15"></path>
                <path d="M10 19L14 19"></path>
            </svg>
        """,
        'wheel_of_fortune': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="gold" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"></circle>
                <circle cx="12" cy="12" r="5"></circle>
                <line x1="12" y1="2" x2="12" y2="22"></line>
                <line x1="2" y1="12" x2="22" y2="12"></line>
                <line x1="4" y1="4" x2="20" y2="20"></line>
                <line x1="4" y1="20" x2="20" y2="4"></line>
            </svg>
        """,
        'astrological_chart': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#4169e1" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M12 2L12 22M2 12L22 12M4 4L20 20M4 20L20 4"></path>
                <circle cx="12" cy="12" r="2"></circle>
            </svg>
        """,
        'mystical_energy': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#9c27b0" stroke-width="1.5">
                <path d="M12 2C10 5 7 5 7 12C7 19 10 19 12 22"></path>
                <path d="M12 2C14 5 17 5 17 12C17 19 14 19 12 22"></path>
                <path d="M7 12H17"></path>
                <path d="M9 7C10 10 14 10 15 7"></path>
                <path d="M9 17C10 14 14 14 15 17"></path>
            </svg>
        """,
        'karmic_cycle': """
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="gold" stroke-width="1.5">
                <path d="M12 22C16.9706 22 21 17.9706 21 13C21 8.02944 16.9706 4 12 4C7.02944 4 3 8.02944 3 13C3 17.9706 7.02944 22 12 22Z"></path>
                <path d="M16 8L12 12L16 16"></path>
                <path d="M8 8L12 12L8 16"></path>
            </svg>
        """
    }
    
    # Return the requested symbol or a default one if not found
    return symbols.get(symbol_name, symbols['pentagram'])

