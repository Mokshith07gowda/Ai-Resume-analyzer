import React, { useState } from 'react';

function Profile({ currentUser, onBack }) {
  const [profilePic, setProfilePic] = useState(currentUser?.profile_pic || null);
  const [isUploading, setIsUploading] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editedName, setEditedName] = useState(currentUser?.full_name || '');
  const [editedEmail, setEditedEmail] = useState(currentUser?.email || '');
  const [saveMessage, setSaveMessage] = useState(null);

  const persistProfile = async ({ fullName, email, photo, successText }) => {
    const response = await fetch(`http://localhost:8000/api/auth/users/${currentUser?.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        full_name: fullName,
        email,
        profile_pic: photo,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Failed to update profile');
    }

    localStorage.setItem('user', JSON.stringify(data.user));
    Object.assign(currentUser, data.user);
    setProfilePic(data.user.profile_pic || null);
    if (successText) {
      setSaveMessage({ type: 'success', text: successText });
      setTimeout(() => setSaveMessage(null), 3000);
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.size > 10 * 1024 * 1024) {
        setSaveMessage({ type: 'error', text: 'File size should be less than 10MB' });
        return;
      }
      
      if (!file.type.startsWith('image/')) {
        setSaveMessage({ type: 'error', text: 'Please upload a valid image file' });
        return;
      }

      setIsUploading(true);
      const reader = new FileReader();
      reader.onloadend = async () => {
        const previousPic = profilePic;
        try {
          setProfilePic(reader.result);
          await persistProfile({
            fullName: currentUser?.full_name || editedName,
            email: currentUser?.email || editedEmail,
            photo: reader.result,
            successText: 'Profile photo updated successfully!'
          });
        } catch (error) {
          setProfilePic(previousPic || null);
          setSaveMessage({ type: 'error', text: error.message || 'Unable to upload profile photo' });
        } finally {
          setIsUploading(false);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const handleRemovePhoto = async () => {
    const previousPic = profilePic;
    setIsUploading(true);
    setProfilePic(null);
    try {
      await persistProfile({
        fullName: currentUser?.full_name || editedName,
        email: currentUser?.email || editedEmail,
        photo: null,
        successText: 'Profile photo removed successfully!'
      });
    } catch (error) {
      setProfilePic(previousPic || null);
      setSaveMessage({ type: 'error', text: error.message || 'Unable to remove profile photo' });
    } finally {
      setIsUploading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
  };

  const handleEdit = () => {
    setIsEditing(true);
    setEditedName(currentUser?.full_name || '');
    setEditedEmail(currentUser?.email || '');
    setSaveMessage(null);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditedName(currentUser?.full_name || '');
    setEditedEmail(currentUser?.email || '');
    setSaveMessage(null);
  };

  const handleSave = async () => {
    if (!editedName.trim()) {
      setSaveMessage({ type: 'error', text: 'Name cannot be empty' });
      return;
    }

    if (!editedEmail.trim()) {
      setSaveMessage({ type: 'error', text: 'Email cannot be empty' });
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(editedEmail)) {
      setSaveMessage({ type: 'error', text: 'Please enter a valid email address' });
      return;
    }

    try {
      await persistProfile({
        fullName: editedName.trim(),
        email: editedEmail.trim(),
        photo: profilePic || null,
        successText: 'Profile updated successfully!'
      });

      setIsEditing(false);
    } catch (error) {
      setSaveMessage({ type: 'error', text: error.message || 'Unable to save profile. Please try again.' });
    }
  };

  return (
    <div className="profile-page">
      <div className="profile-header-section">
        <button className="back-button" onClick={onBack}>
          ← Back to Dashboard
        </button>
        <h1 className="profile-page-title">My Profile</h1>
        <p className="profile-page-subtitle">Manage your account information and preferences</p>
      </div>

      <div className="profile-content">
        <div className="profile-card">
          <div className="profile-pic-section">
            <div className="profile-pic-container">
              {profilePic ? (
                <img src={profilePic} alt="Profile" className="profile-pic-image" />
              ) : (
                <div className="profile-pic-placeholder">
                  {currentUser?.full_name?.charAt(0).toUpperCase() || 'U'}
                </div>
              )}
            </div>
            
            <div className="profile-pic-actions">
              <label htmlFor="profile-pic-upload" className="upload-button">
                {isUploading ? 'Uploading...' : 'Upload Photo'}
              </label>
              <input
                id="profile-pic-upload"
                type="file"
                accept="image/*"
                onChange={handleFileUpload}
                disabled={isUploading}
                style={{ display: 'none' }}
              />
              {profilePic && (
                <button className="remove-button" onClick={handleRemovePhoto}>
                  Remove Photo
                </button>
              )}
            </div>
            <p className="profile-pic-hint">Max file size: 10MB. Accepted formats: JPG, PNG, GIF, WEBP</p>
          </div>

          <div className="profile-info-section">
            <div className="section-header">
              <h2 className="section-title">Personal Information</h2>
              {!isEditing ? (
                <button className="edit-profile-button" onClick={handleEdit}>
                  ✎ Edit Profile
                </button>
              ) : (
                <div className="edit-actions">
                  <button className="save-profile-button" onClick={handleSave}>
                    ✓ Save
                  </button>
                  <button className="cancel-profile-button" onClick={handleCancel}>
                    ✕ Cancel
                  </button>
                </div>
              )}
            </div>

            {saveMessage && (
              <div className={`profile-save-message ${saveMessage.type}`}>
                {saveMessage.text}
              </div>
            )}
            
            <div className="info-group">
              <label className="info-label">Full Name</label>
              {isEditing ? (
                <input
                  type="text"
                  className="info-input"
                  value={editedName}
                  onChange={(e) => setEditedName(e.target.value)}
                  placeholder="Enter your full name"
                />
              ) : (
                <div className="info-value">{currentUser?.full_name || 'Not provided'}</div>
              )}
            </div>

            <div className="info-group">
              <label className="info-label">Email Address</label>
              {isEditing ? (
                <input
                  type="email"
                  className="info-input"
                  value={editedEmail}
                  onChange={(e) => setEditedEmail(e.target.value)}
                  placeholder="Enter your email address"
                />
              ) : (
                <div className="info-value">{currentUser?.email || 'Not provided'}</div>
              )}
            </div>

            <div className="info-group">
              <label className="info-label">Account Status</label>
              <div className="info-value">
                <span className={`status-badge-profile ${currentUser?.is_active ? 'active' : 'inactive'}`}>
                  {currentUser?.is_active ? '● Active' : '● Inactive'}
                </span>
              </div>
            </div>

            <div className="info-group">
              <label className="info-label">Member Since</label>
              <div className="info-value member-since">
                {formatDate(currentUser?.created_at)}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;
