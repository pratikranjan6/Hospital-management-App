/**
 * Appointment Slot Manager
 * Handles generation and management of appointment slots
 * Each slot is 30 minutes by default
 */

export const SLOT_CONFIG = {
  // Working hours
  START_HOUR: 9, // 09:00 AM
  END_HOUR: 17, // 05:00 PM
  
  // Slot duration in minutes
  SLOT_DURATION_MINUTES: 30,
  
  // Days to show availability
  DAYS_TO_SHOW: 7,
  
  // Weekend unavailability
  WEEKEND_UNAVAILABLE: true // If true, Saturday (6) and Sunday (0) are unavailable
}

/**
 * Generate time slots for a single day
 * @param {Date} date - The date to generate slots for
 * @returns {Array} Array of time slot objects
 */
export function generateDaySlots(date, startHour = SLOT_CONFIG.START_HOUR, endHour = SLOT_CONFIG.END_HOUR) {
  const slots = []
  const slotDuration = SLOT_CONFIG.SLOT_DURATION_MINUTES

  for (let hour = startHour; hour < endHour; hour++) {
    for (let minute = 0; minute < 60; minute += slotDuration) {
      const startTime = `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`
      
      let endHour = hour
      let endMinute = minute + slotDuration

      if (endMinute >= 60) {
        endHour += 1
        endMinute = 0
      }

      const endTime = `${String(endHour).padStart(2, '0')}:${String(endMinute).padStart(2, '0')}`

      slots.push({
        startTime,
        endTime,
        duration: slotDuration // in minutes
      })
    }
  }

  return slots
}

/**
 * Check if a date is available (not a weekend)
 * @param {Date} date - The date to check
 * @returns {boolean} True if available, false otherwise
 */
export function isDateAvailable(date) {
  if (!SLOT_CONFIG.WEEKEND_UNAVAILABLE) {
    return true
  }

  const dayOfWeek = date.getDay()
  // Sunday = 0, Saturday = 6
  return dayOfWeek !== 0 && dayOfWeek !== 6
}

/**
 * Format time from HH:MM format to readable format
 * @param {string} time - Time in HH:MM format
 * @returns {string} Formatted time (e.g., "09:00 AM")
 */
export function formatTime(time) {
  const [hours, minutes] = time.split(':')
  const hour = parseInt(hours)
  const period = hour >= 12 ? 'PM' : 'AM'
  const displayHour = hour > 12 ? hour - 12 : hour === 0 ? 12 : hour

  return `${displayHour}:${minutes} ${period}`
}

/**
 * Get total number of slots per day
 * @returns {number} Number of slots
 */
export function getSlotsPerDay() {
  const startHour = SLOT_CONFIG.START_HOUR
  const endHour = SLOT_CONFIG.END_HOUR
  const slotDuration = SLOT_CONFIG.SLOT_DURATION_MINUTES
  
  const totalMinutes = (endHour - startHour) * 60
  return totalMinutes / slotDuration
}

/**
 * Get total number of slots for 7 days
 * @returns {number} Total slots
 */
export function getTotalSlots() {
  return getSlotsPerDay() * SLOT_CONFIG.DAYS_TO_SHOW
}

export default {
  SLOT_CONFIG,
  generateDaySlots,
  isDateAvailable,
  formatTime,
  getSlotsPerDay,
  getTotalSlots
}
