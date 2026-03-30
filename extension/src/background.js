/**
 * Service Worker - Background script for PrimeAI extension
 */

const API_URL = 'http://localhost:8000/api';

// Initialize on install
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ extensionVersion: chrome.runtime.getVersion() });
});

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'checkSubscription') {
    validateSubscription().then(valid => {
      sendResponse({ valid });
    });
    return true;
  }

  if (request.action === 'getAuthToken') {
    chrome.storage.local.get(['authToken'], (items) => {
      sendResponse({ token: items.authToken });
    });
    return true;
  }

  if (request.action === 'switchProfile') {
    activateProfile(request.profileId).then(() => {
      sendResponse({ updated: true });
    });
    return true;
  }
});

// Validate subscription with backend
async function validateSubscription() {
  return new Promise((resolve) => {
    chrome.storage.local.get(['authToken'], async (items) => {
      if (!items.authToken) {
        resolve(false);
        return;
      }

      try {
        const response = await fetch(`${API_URL}/extension/validate`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${items.authToken}`,
            'Content-Type': 'application/json'
          }
        });

        resolve(response.ok);
      } catch (error) {
        console.error('Validation error:', error);
        resolve(false);
      }
    });
  });
}

// Activate profile and load configuration
async function activateProfile(profileId) {
  return new Promise((resolve) => {
    chrome.storage.local.get(['authToken'], async (items) => {
      try {
        const response = await fetch(`${API_URL}/extension/config`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${items.authToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ profile_id: profileId })
        });

        const config = await response.json();

        // Store config and broadcast to all tabs
        chrome.storage.local.set({
          activeProfile: profileId,
          stealthConfig: config
        });

        // Send config to all active tabs
        chrome.tabs.query({}, (tabs) => {
          tabs.forEach(tab => {
            chrome.tabs.sendMessage(tab.id, {
              action: 'updateConfig',
              config: config,
              interviewMode: config.interview_mode
            }).catch(() => {});
          });
        });

        resolve();
      } catch (error) {
        console.error('Error activating profile:', error);
        resolve();
      }
    });
  });
}

// Auto-load active profile on startup
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'loading') {
    chrome.storage.local.get(['activeProfile'], (items) => {
      if (items.activeProfile) {
        chrome.tabs.sendMessage(tabId, {
          action: 'loadConfig',
          profileId: items.activeProfile
        }).catch(() => {});
      }
    });
  }
});

// Periodic subscription validation (every hour)
setInterval(() => {
  validateSubscription().then(valid => {
    if (!valid) {
      chrome.storage.local.set({ subscriptionExpired: true });
    }
  });
}, 3600000);
