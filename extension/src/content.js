/**
 * Content Script - Injects stealth code into all pages
 */

// Inject stealth script before page loads
function injectStealth() {
  const script = document.createElement('script');
  script.src = chrome.runtime.getURL('src/stealth.js');
  script.onload = function() {
    this.remove();
  };
  (document.head || document.documentElement).appendChild(script);
}

// Inject on document_start
injectStealth();

// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getConfig') {
    chrome.storage.local.get(['authToken', 'activeProfile'], (items) => {
      sendResponse({
        token: items.authToken,
        profileId: items.activeProfile
      });
    });
  }

  if (request.action === 'updateConfig') {
    // Pass config to stealth script via window object
    window.__stealthConfig = request.config;
    window.__interviewMode = request.interviewMode;
    sendResponse({ updated: true });
  }
});

// Check subscription on page load
chrome.runtime.sendMessage({ action: 'checkSubscription' }, (response) => {
  if (response && !response.valid) {
    console.warn('Subscription expired or invalid');
  }
});
