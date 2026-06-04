import api from './index'

export const getProjects = (params) => api.get('/projects/', { params })
export const getProject = (id) => api.get(`/projects/${id}/`)
export const createProject = (data) => api.post('/projects/', data)
export const updateProject = (id, data) => api.patch(`/projects/${id}/`, data)
export const deleteProject = (id) => api.delete(`/projects/${id}/`)
export const joinProject = (id) => api.post(`/projects/${id}/join/`)
export const leaveProject = (id) => api.post(`/projects/${id}/leave/`)
