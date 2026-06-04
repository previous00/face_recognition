import api from './index'

export const getPapers = (params) => api.get('/papers/', { params })
export const getPaper = (id) => api.get(`/papers/${id}/`)
export const createPaper = (data) => api.post('/papers/', data, {
  headers: { 'Content-Type': 'multipart/form-data' }
})
export const updatePaper = (id, data) => api.patch(`/papers/${id}/`, data, {
  headers: { 'Content-Type': 'multipart/form-data' }
})
export const deletePaper = (id) => api.delete(`/papers/${id}/`)
export const downloadPaper = (id) => api.get(`/papers/${id}/download/`, { responseType: 'blob' })
