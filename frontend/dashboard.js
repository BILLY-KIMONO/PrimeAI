/**
 * Dashboard JavaScript
 */

const API_URL = 'http://localhost:8000/api';
let currentUser = null;
let currentSubscription = null;
const authToken = localStorage.getItem('authToken');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  if (!authToken) {
    window.location.href = 'login.html';
    return;
  }

  loadUserInfo();
  loadSubscription();
  loadProfiles();
});

async function loadUserInfo() {
  try {
    // Extract user ID from token JWT payload
    const payload = JSON.parse(atob(authToken.split('.')[1]));
    
    const response = await fetch(`${API_URL}/auth/me`, {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });

    currentUser = await response.json();
    document.getElementById('userEmail').textContent = currentUser.email;
  } catch (error) {
    console.error('Error loading user:', error);
  }
}

async function loadSubscription() {
  try {
    const response = await fetch(`${API_URL}/subscriptions/active`, {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });

    if (!response.ok) {
      document.getElementById('subscriptionStatus').innerHTML = '❌ No active subscription';
      return;
    }

    currentSubscription = await response.json();
    const endDate = new Date(currentSubscription.end_date);
    const today = new Date();
    const daysLeft = Math.ceil((endDate - today) / (1000 * 60 * 60 * 24));

    const statusEl = document.getElementById('subscriptionStatus');
    const statusClass = currentSubscription.plan_type === 'trial' ? 'subscription-trial' : 'subscription-active';
    statusEl.className = 'subscription-status ' + statusClass;
    
    let statusText = currentSubscription.plan_type === 'trial' ? 'FREE TRIAL' : 'ACTIVE';
    statusEl.textContent = `✅ ${statusText} - ${daysLeft} days remaining`;

    // Update details
    document.querySelector('.stat-label:nth-of-type(1)').nextElementSibling.textContent = 
      currentSubscription.plan_type.toUpperCase();
    document.querySelector('.stat-label:nth-of-type(2)').nextElementSibling.textContent =
      `${currentSubscription.api_calls_used} / ${currentSubscription.api_calls_limit}`;
    document.querySelector('.stat-label:nth-of-type(3)').nextElementSibling.textContent =
      new Date(currentSubscription.end_date).toLocaleDateString();
  } catch (error) {
    console.error('Error loading subscription:', error);
  }
}

async function loadProfiles() {
  try {
    const response = await fetch(`${API_URL}/devices/list`, {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });

    const profiles = await response.json();
    document.getElementById('profileCount').textContent = profiles.length;

    const profilesList = document.getElementById('profilesList');
    
    if (!profiles || profiles.length === 0) {
      profilesList.innerHTML = `
        <p style="text-align: center; color: #64748b; padding: 40px 0;">
          No profiles yet. Create one to get started!
        </p>
      `;
      return;
    }

    profilesList.innerHTML = profiles.map(profile => `
      <div class="profile-card">
        <div class="profile-info">
          <h3>
            ${profile.interview_mode ? '🎬 ' : ''}${profile.profile_name}
          </h3>
          <div class="profile-features">
            ${profile.interview_mode ? '<span class="profile-badge">Interview Mode</span>' : ''}
            ${profile.canvas_noise ? '<span class="profile-badge">Canvas Spoof</span>' : ''}
            ${profile.webgl_noise ? '<span class="profile-badge">WebGL Spoof</span>' : ''}
          </div>
        </div>
        <div style="display: flex; gap: 8px;">
          <button class="btn btn-secondary" onclick="editProfile(${profile.id})">Edit</button>
          <button class="btn btn-danger" onclick="deleteProfile(${profile.id})">Delete</button>
        </div>
      </div>
    `).join('');
  } catch (error) {
    console.error('Error loading profiles:', error);
  }
}

async function createProfile(event) {
  event.preventDefault();
  const form = event.target;
  const formData = new FormData(form);

  const [width, height] = formData.get('screen_res').split('x');

  const profileData = {
    profile_name: formData.get('profile_name'),
    timezone: formData.get('timezone'),
    language: formData.get('language'),
    screen_width: parseInt(width),
    screen_height: parseInt(height),
    canvas_noise: formData.get('canvas_noise') === 'true',
    webgl_noise: formData.get('webgl_noise') === 'true',
    random_mouse_movements: formData.get('random_mouse_movements') === 'true',
    keyboard_delays: formData.get('keyboard_delays') === 'true',
    webrtc_leak_prevention: true,
    interview_mode: formData.get('interview_mode') === 'true'
  };

  try {
    const response = await fetch(`${API_URL}/devices/create`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(profileData)
    });

    if (response.ok) {
      showAlert('Profile created successfully!', 'success');
      closeModal('createProfileModal');
      form.reset();
      loadProfiles();
    } else {
      showAlert('Failed to create profile', 'error');
    }
  } catch (error) {
    console.error('Error creating profile:', error);
    showAlert('Error creating profile', 'error');
  }
}

async function deleteProfile(profileId) {
  if (!confirm('Are you sure you want to delete this profile?')) return;

  try {
    const response = await fetch(`${API_URL}/devices/${profileId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });

    if (response.ok) {
      showAlert('Profile deleted', 'success');
      loadProfiles();
    }
  } catch (error) {
    console.error('Error deleting profile:', error);
  }
}

function editProfile(profileId) {
  alert('Edit profile feature coming soon!');
}

function setDeviceDefaults(deviceType) {
  const defaults = {
    'windows': { res: '1920x1080', tz: 'America/New_York' },
    'macos': { res: '1440x900', tz: 'America/New_York' },
    'linux': { res: '1920x1200', tz: 'UTC' },
    'iphone': { res: '390x844', tz: 'UTC' },
    'android': { res: '1080x2340', tz: 'UTC' },
  };

  if (defaults[deviceType]) {
    document.querySelector('[name="screen_res"]').value = defaults[deviceType].res;
    document.querySelector('[name="timezone"]').value = defaults[deviceType].tz;
  }
}

function showCreateProfileModal() {
  document.getElementById('createProfileModal').classList.add('active');
}

function showPricingModal() {
  document.getElementById('pricingModal').classList.add('active');
}

function closeModal(modalId) {
  document.getElementById(modalId).classList.remove('active');
}

function upgradePlan() {
  alert('Payment integration coming soon! For now, your trial is active.');
}

function logout() {
  localStorage.removeItem('authToken');
  window.location.href = 'login.html';
}

function showAlert(message, type = 'info') {
  const alertsDiv = document.getElementById('alerts');
  const alert = document.createElement('div');
  alert.className = `alert alert-${type}`;
  alert.textContent = message;
  alertsDiv.appendChild(alert);
  
  setTimeout(() => alert.remove(), 5000);
}

// Close modals when clicking outside
document.querySelectorAll('.modal').forEach(modal => {
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.remove('active');
    }
  });
});
