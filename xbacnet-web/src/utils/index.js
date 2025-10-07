/**
 * Utility functions for XBACnet Web Management Interface
 */

import dayjs from 'dayjs'
import { ElMessage } from 'element-plus'

/**
 * Format date and time
 * @param {Date|string} date - Date to format
 * @param {string} format - Format string
 * @returns {string} Formatted date string
 */
export function formatDateTime(date, format = 'YYYY-MM-DD HH:mm:ss') {
  return dayjs(date).format(format)
}

/**
 * Format date only
 * @param {Date|string} date - Date to format
 * @returns {string} Formatted date string
 */
export function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD')
}

/**
 * Format time only
 * @param {Date|string} date - Date to format
 * @returns {string} Formatted time string
 */
export function formatTime(date) {
  return dayjs(date).format('HH:mm:ss')
}

/**
 * Get relative time (e.g., "2 hours ago")
 * @param {Date|string} date - Date to format
 * @returns {string} Relative time string
 */
export function getRelativeTime(date) {
  return dayjs(date).fromNow()
}

/**
 * Debounce function
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
export function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

/**
 * Throttle function
 * @param {Function} func - Function to throttle
 * @param {number} limit - Limit time in milliseconds
 * @returns {Function} Throttled function
 */
export function throttle(func, limit) {
  let inThrottle
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

/**
 * Copy text to clipboard
 * @param {string} text - Text to copy
 * @returns {Promise<boolean>} Success status
 */
export async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text)
    ElMessage.success('Copied to clipboard')
    return true
  } catch (error) {
    console.error('Failed to copy to clipboard:', error)
    ElMessage.error('Failed to copy to clipboard')
    return false
  }
}

/**
 * Download data as file
 * @param {string} data - Data to download
 * @param {string} filename - Filename
 * @param {string} type - MIME type
 */
export function downloadFile(data, filename, type = 'text/plain') {
  const blob = new Blob([data], { type })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

/**
 * Export data as JSON
 * @param {Object} data - Data to export
 * @param {string} filename - Filename
 */
export function exportAsJSON(data, filename) {
  const jsonString = JSON.stringify(data, null, 2)
  downloadFile(jsonString, filename, 'application/json')
}

/**
 * Export data as CSV
 * @param {Array} data - Array of objects
 * @param {string} filename - Filename
 */
export function exportAsCSV(data, filename) {
  if (!data.length) return
  
  const headers = Object.keys(data[0])
  const csvContent = [
    headers.join(','),
    ...data.map(row => 
      headers.map(header => {
        const value = row[header]
        return typeof value === 'string' && value.includes(',') 
          ? `"${value}"` 
          : value
      }).join(',')
    )
  ].join('\n')
  
  downloadFile(csvContent, filename, 'text/csv')
}

/**
 * Generate UUID
 * @returns {string} UUID string
 */
export function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0
    const v = c === 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
}

/**
 * Validate email address
 * @param {string} email - Email to validate
 * @returns {boolean} Validation result
 */
export function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

/**
 * Validate IP address
 * @param {string} ip - IP address to validate
 * @returns {boolean} Validation result
 */
export function validateIP(ip) {
  const re = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/
  return re.test(ip)
}

/**
 * Format file size
 * @param {number} bytes - Size in bytes
 * @returns {string} Formatted size string
 */
export function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * Get BACnet object type display name
 * @param {string} type - BACnet object type
 * @returns {string} Display name
 */
export function getBACnetObjectTypeName(type) {
  const typeMap = {
    'analog_input': 'Analog Input',
    'analog_output': 'Analog Output',
    'analog_value': 'Analog Value',
    'binary_input': 'Binary Input',
    'binary_output': 'Binary Output',
    'binary_value': 'Binary Value',
    'multi_state_input': 'Multi-state Input',
    'multi_state_output': 'Multi-state Output',
    'multi_state_value': 'Multi-state Value'
  }
  
  return typeMap[type] || type
}

/**
 * Get BACnet event state display name
 * @param {string} state - Event state
 * @returns {string} Display name
 */
export function getBACnetEventStateName(state) {
  const stateMap = {
    'normal': 'Normal',
    'fault': 'Fault',
    'offnormal': 'Off Normal',
    'highLimit': 'High Limit',
    'lowLimit': 'Low Limit'
  }
  
  return stateMap[state] || state
}

/**
 * Get BACnet event state color
 * @param {string} state - Event state
 * @returns {string} Color type for Element Plus
 */
export function getBACnetEventStateColor(state) {
  const colorMap = {
    'normal': 'success',
    'fault': 'danger',
    'offnormal': 'warning',
    'highLimit': 'warning',
    'lowLimit': 'warning'
  }
  
  return colorMap[state] || 'info'
}

/**
 * Parse status flags
 * @param {string} flags - Status flags string (4 digits)
 * @returns {Object} Parsed status flags
 */
export function parseStatusFlags(flags) {
  if (!flags || flags.length !== 4) {
    return {
      inAlarm: false,
      fault: false,
      overridden: false,
      outOfService: false
    }
  }
  
  return {
    inAlarm: flags[0] === '1',
    fault: flags[1] === '1',
    overridden: flags[2] === '1',
    outOfService: flags[3] === '1'
  }
}

/**
 * Format status flags
 * @param {Object} flags - Status flags object
 * @returns {string} Formatted status flags string
 */
export function formatStatusFlags(flags) {
  const inAlarm = flags.inAlarm ? '1' : '0'
  const fault = flags.fault ? '1' : '0'
  const overridden = flags.overridden ? '1' : '0'
  const outOfService = flags.outOfService ? '1' : '0'
  
  return `${inAlarm}${fault}${overridden}${outOfService}`
}

/**
 * Sleep function
 * @param {number} ms - Milliseconds to sleep
 * @returns {Promise} Promise that resolves after specified time
 */
export function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * Retry function with exponential backoff
 * @param {Function} fn - Function to retry
 * @param {number} maxRetries - Maximum number of retries
 * @param {number} baseDelay - Base delay in milliseconds
 * @returns {Promise} Promise that resolves with function result
 */
export async function retry(fn, maxRetries = 3, baseDelay = 1000) {
  let lastError
  
  for (let i = 0; i <= maxRetries; i++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error
      
      if (i === maxRetries) {
        throw lastError
      }
      
      const delay = baseDelay * Math.pow(2, i)
      await sleep(delay)
    }
  }
}

/**
 * Deep clone object
 * @param {*} obj - Object to clone
 * @returns {*} Cloned object
 */
export function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') {
    return obj
  }
  
  if (obj instanceof Date) {
    return new Date(obj.getTime())
  }
  
  if (obj instanceof Array) {
    return obj.map(item => deepClone(item))
  }
  
  if (typeof obj === 'object') {
    const clonedObj = {}
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        clonedObj[key] = deepClone(obj[key])
      }
    }
    return clonedObj
  }
}
