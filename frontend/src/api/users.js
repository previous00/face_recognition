import api from './index'

export const getUsers = (params) => api.get('/users/', { params })
export const getUser = (id) => api.get(`/users/${id}/`)
export const updateUser = (id, data) => api.patch(`/users/${id}/`, data)
export const setUserRole = (id, role) => api.post(`/users/${id}/set_role/`, { role })
export const toggleUserActive = (id) => api.post(`/users/${id}/toggle_active/`)
