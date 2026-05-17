export function getApiBase() {
  return ''
}

export function getAuthHeader() {
  const token = localStorage.getItem('token')
  if (token) {
    return {
      'Authorization': `Bearer ${token}`
    }
  }
  return {}
}

export function isAuthenticated() {
  return !!localStorage.getItem('token')
}

export function getRole() {
  return localStorage.getItem('role') || ''
}
