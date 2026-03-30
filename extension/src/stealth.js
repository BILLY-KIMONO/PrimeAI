/**
 * STEALTH.JS - Core anti-detect library
 * This file contains all the fingerprint spoofing and detection bypass techniques
 * It runs in the isolated world to prevent detection
 */

(function() {
  'use strict';

  // Prevent console access during interview
  if (window.__interviewMode) {
    Object.defineProperty(window, 'console', {
      get: () => ({
        log: () => {},
        error: () => {},
        warn: () => {},
        info: () => {},
        debug: () => {},
        trace: () => {},
        table: () => {},
        clear: () => {},
        time: () => {},
        timeEnd: () => {},
        group: () => {},
        groupEnd: () => {},
        group: () => {},
        groupCollapsed: () => {},
      }),
      set: () => {},
    });
  }

  // Randomization utilities
  const Random = {
    delay: () => Math.random() * 500 + 100,
    jitter: (value, percent = 0.1) => value * (1 + (Math.random() - 0.5) * 2 * percent),
    element: (arr) => arr[Math.floor(Math.random() * arr.length)],
  };

  // User agents pool for realism
  const USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
    'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36',
  ];

  // === NAVIGATOR SPOOFING ===
  const navigatorOverrides = {
    userAgent: window.__stealthConfig?.user_agent || Random.element(USER_AGENTS),
    platform: window.__stealthConfig?.platform || 'Linux x86_64',
    vendor: window.__stealthConfig?.browser_vendor || 'Google Inc.',
    language: window.__stealthConfig?.language || 'en-US',
    hardwareConcurrency: window.__stealthConfig?.cpu_cores || 8,
    deviceMemory: window.__stealthConfig?.device_memory || 8,
    maxTouchPoints: window.__stealthConfig?.max_touch_points || 0,
  };

  // Override navigator properties
  Object.keys(navigatorOverrides).forEach(key => {
    try {
      Object.defineProperty(navigator, key, {
        get: () => navigatorOverrides[key],
        set: () => {},
      });
    } catch (e) {}
  });

  // === SCREEN SPOOFING ===
  const screenOverrides = {
    width: window.__stealthConfig?.screen_width || 1920,
    height: window.__stealthConfig?.screen_height || 1080,
    availWidth: window.__stealthConfig?.screen_width || 1920,
    availHeight: window.__stealthConfig?.screen_height || 1040,
    colorDepth: window.__stealthConfig?.screen_color_depth || 24,
    pixelDepth: window.__stealthConfig?.screen_color_depth || 24,
  };

  Object.keys(screenOverrides).forEach(key => {
    Object.defineProperty(screen, key, {
      get: () => screenOverrides[key],
      set: () => {},
    });
  });

  // === CANVAS FINGERPRINTING PREVENTION ===
  if (window.__stealthConfig?.canvas_noise) {
    const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
    HTMLCanvasElement.prototype.toDataURL = function(type) {
      // Add noise to canvas to prevent fingerprinting
      const ctx = this.getContext('2d');
      const imageData = ctx.getImageData(0, 0, this.width, this.height);
      const data = imageData.data;
      
      for (let i = 0; i < data.length; i += 4) {
        if (Math.random() > 0.95) {
          data[i] ^= Math.floor(Math.random() * 256);
          data[i + 1] ^= Math.floor(Math.random() * 256);
          data[i + 2] ^= Math.floor(Math.random() * 256);
        }
      }
      
      ctx.putImageData(imageData, 0, 0);
      return originalToDataURL.call(this, type);
    };
  }

  // === WEBGL FINGERPRINTING PREVENTION ===
  if (window.__stealthConfig?.webgl_noise) {
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {
      if (parameter === 37445) {
        return 'Intel Inc.';
      }
      if (parameter === 37446) {
        return 'Intel Iris OpenGL Engine';
      }
      return getParameter.call(this, parameter);
    };

    // WebGL2 support
    if (WebGL2RenderingContext) {
      const getParameter2 = WebGL2RenderingContext.prototype.getParameter;
      WebGL2RenderingContext.prototype.getParameter = function(parameter) {
        if (parameter === 37445) {
          return 'Intel Inc.';
        }
        if (parameter === 37446) {
          return 'Intel Iris OpenGL Engine';
        }
        return getParameter2.call(this, parameter);
      };
    }
  }

  // === WEBRTC LEAK PREVENTION ===
  if (window.__stealthConfig?.webrtc_leak_prevention) {
    const origRTCPeerConnection = window.RTCPeerConnection;
    
    function blockWebRTC() {
      if (window.RTCPeerConnection) {
        window.RTCPeerConnection = class {
          constructor() {
            throw new Error('RTCPeerConnection blocked');
          }
        };
        window.RTCPeerConnection.prototype = origRTCPeerConnection.prototype;
      }
    }

    // Force mDNS mode to prevent WebRTC leaks
    const pc = new RTCPeerConnection({ iceServers: [] });
    pc.createDataChannel('');
    pc.createOffer().then(offer => pc.setLocalDescription(offer));
  }

  // === TIMEZONE SPOOFING ===
  if (window.__stealthConfig?.timezone) {
    const timeZone = window.__stealthConfig.timezone;
    const DateTimeFormat = Intl.DateTimeFormat;
    
    Intl.DateTimeFormat = class extends DateTimeFormat {
      constructor(locales, options) {
        options = options || {};
        options.timeZone = timeZone;
        super(locales, options);
      }
    };
    
    try {
      Object.defineProperty(Date.prototype, 'getTimezoneOffset', {
        value: function() {
          new DateTimeFormat('en-US', { timeZone }).format(this);
          return -(new Date().getTime() - new Date(new Date().toLocaleString('en-US', { timeZone })).getTime()) / 60000;
        }
      });
    } catch (e) {}
  }

  // === BEHAVIOR RANDOMIZATION (INTERVIEW MODE) ===
  if (window.__stealthConfig?.random_mouse_movements) {
    let mouseX = 0, mouseY = 0;
    
    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    }, true);

    // Simulate realistic mouse movement patterns
    setInterval(() => {
      if (Math.random() > 0.8) {
        const event = new MouseEvent('mousemove', {
          bubbles: true,
          clientX: mouseX + (Math.random() - 0.5) * 10,
          clientY: mouseY + (Math.random() - 0.5) * 10,
        });
        document.dispatchEvent(event);
      }
    }, 500 + Math.random() * 500);
  }

  // === KEYBOARD TIMING RANDOMIZATION ===
  if (window.__stealthConfig?.keyboard_delays) {
    const originalAddEventListener = EventTarget.prototype.addEventListener;
    
    EventTarget.prototype.addEventListener = function(type, listener, options) {
      if (type === 'keydown' || type === 'keyup' || type === 'keypress') {
        const wrappedListener = function(event) {
          // Add realistic response delays
          setTimeout(() => {
            listener.call(this, event);
          }, Random.jitter(50, 0.3));
        };
        return originalAddEventListener.call(this, type, wrappedListener, options);
      }
      return originalAddEventListener.call(this, type, listener, options);
    };
  }

  // === PLUGIN SPOOFING ===
  Object.defineProperty(navigator, 'plugins', {
    get: () => [
      {
        name: 'Chrome PDF Plugin',
        description: 'Portable Document Format',
        filename: 'internal-pdf-viewer',
        version: '1.0',
      },
      {
        name: 'Chrome PDF Viewer',
        description: '',
        filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai',
        version: '1.0',
      },
    ],
    set: () => {},
  });

  // === PERMISSION SPOOFING ===
  const originalQuery = window.navigator.permissions.query;
  window.navigator.permissions.query = (parameters) => {
    if (parameters.name === 'notifications') {
      return Promise.resolve({ state: Notification.permission });
    }
    return originalQuery(parameters);
  };

  // === LANGUAGE OVERRIDE ===
  Object.defineProperty(navigator, 'languages', {
    get: () => [navigatorOverrides.language],
    set: () => {},
  });

  // === DISABLE DEVELOPER TOOLS ===
  if (window.__stealthConfig?.interview_mode) {
    // Detect and disable DevTools
    const threshold = 160;
    setInterval(() => {
      if (window.outerHeight - window.innerHeight > threshold || 
          window.outerWidth - window.innerWidth > threshold) {
        document.body.innerHTML = 'DevTools detected. This application requires DevTools to be closed.';
        window.location.reload();
      }
    }, 500);

    // Disable common keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && e.key === 'I') ||
          (e.ctrlKey && e.shiftKey && e.key === 'C') || 
          (e.metaKey && e.altKey && e.key === 'I')) {
        e.preventDefault();
        e.stopPropagation();
      }
    });

    // Block right-click
    document.addEventListener('contextmenu', (e) => {
      e.preventDefault();
    });
  }

  // === PERFORMANCE API RANDOMIZATION ===
  const originalPerformance = window.performance.getEntriesByType;
  window.performance.getEntriesByType = function(type) {
    const entries = originalPerformance.call(this, type);
    if (type === 'navigation' || type === 'resource') {
      entries.forEach(entry => {
        entry.duration = Random.jitter(entry.duration, 0.2);
      });
    }
    return entries;
  };

  // === HIDE EXTENSION DETECTION ===
  window.__extensionDetected = false;
  
  // Override chrome object
  if (typeof chrome !== 'undefined') {
    Object.defineProperty(window, 'chrome', {
      get: () => undefined,
      set: () => {},
    });
  }

  console.log('🔒 AntiDetect stealth mode activated');
})();
