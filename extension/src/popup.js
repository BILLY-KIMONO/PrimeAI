/**
 * Popup Script - UI interactions
 */

const API_URL = 'http://localhost:8000/api';

// Load profiles on popup open
document.addEventListener('DOMContentLoaded', loadProfiles);

async function loadProfiles() {
  chrome.storage.local.get(['authToken', 'activeProfile'], async (items) => {
    if (!items.authToken) {
      showLoginPrompt();
      return;
    }

    try {
      const response = await fetch(`${API_URL}/devices/list`, {
        headers: {
          'Authorization': `Bearer ${items.authToken}`
        }
      });

      if (!response.ok) {
        if (response.status === 401) {
          chrome.storage.local.remove('authToken');
          showLoginPrompt();
        }
        return;
      }

      const profiles = await response.json();
      renderProfiles(profiles, items.activeProfile);
      
      // Check subscription
      await checkSubscriptionStatus(items.authToken, items.activeProfile);
    } catch (error) {
      console.error('Error loading profiles:', error);
    }
  });
}

function renderProfiles(profiles, activeId) {
  const profileList = document.getElementById('profileList');
  
  if (!profiles || profiles.length === 0) {
    profileList.innerHTML = `
      <div class="profile-item">
        No profiles yet. Create one in dashboard.
      </div>
    `;
    return;
  }

  profileList.innerHTML = profiles.map(profile => `
    <div class="profile-item ${profile.id === activeId ? 'active' : ''}" 
         onclick="activateProfile(${profile.id})">
      <div class="profile-name">
        ${profile.interview_mode ? '🎬 ' : ''}${profile.profile_name}
      </div>
      <div class="profile-settings">
        Stealth: ${profile.interview_mode ? 'HARD' : 'SOFT'}
      </div>
    </div>
  `).join('');

  // Update status
  if (activeId) {
    const status = document.getElementById('status');
    const badge = status.querySelector('.status-badge');
    badge.className = 'status-badge status-active';
    badge.textContent = 'ACTIVE';
    status.querySelector('.status-text').textContent = 'Spoofing enabled';

    // Show interview mode indicator
    const activeProfile = profiles.find(p => p.id === activeId);
    if (activeProfile && activeProfile.interview_mode) {
      document.getElementById('interviewMode').style.display = 'block';
    }
  }
}

async function activateProfile(profileId) {
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

      if (response.ok) {
        const config = await response.json();
        chrome.storage.local.set({
          activeProfile: profileId,
          stealthConfig: config
        });

        // Reload profiles to show active state
        loadProfiles();

        // Notify all tabs
        chrome.tabs.query({}, (tabs) => {
          tabs.forEach(tab => {
            chrome.tabs.sendMessage(tab.id, {
              action: 'updateConfig',
              config: config,
              interviewMode: config.interview_mode
            }).catch(() => {});
          });
        });
      }
    } catch (error) {
      console.error('Error activating profile:', error);
    }
  });
}

async function checkSubscriptionStatus(token, profileId) {
  try {
    const response = await fetch(`${API_URL}/subscriptions/active`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      document.getElementById('warning').style.display = 'block';
      return false;
    }

    const subscription = await response.json();
    
    // Check if trial or days remaining
    const endDate = new Date(subscription.end_date);
    const today = new Date();
    const daysLeft = Math.ceil((endDate - today) / (1000 * 60 * 60 * 24));

    if (daysLeft <= 0) {
      document.getElementById('warning').style.display = 'block';
      return false;
    }

    return true;
  } catch (error) {
    console.error('Error checking subscription:', error);
    return false;
  }
}

function showLoginPrompt() {
  document.getElementById('profileList').innerHTML = `
    <div class="profile-item">
      <div class="profile-name">Not logged in</div>
      <div class="profile-settings">
        <button class="btn-primary" onclick="openDashboard()" style="margin-top: 8px; width: 100%;">
          Login Now
        </button>
      </div>
    </div>
  `;
}

function openDashboard() {
  chrome.tabs.create({ url: 'http://localhost:3000' });
}

function openSettings() {
  chrome.tabs.create({ url: 'http://localhost:3000/settings' });
}
