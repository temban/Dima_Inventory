export const required = (value: any): boolean | string => {
  if (value === null || value === undefined || value === '') {
    return 'This field is required'
  }
  return true
}

export const minLength = (min: number) => {
  return (value: string): boolean | string => {
    if (value.length < min) {
      return `Must be at least ${min} characters`
    }
    return true
  }
}

export const maxLength = (max: number) => {
  return (value: string): boolean | string => {
    if (value.length > max) {
      return `Must be less than ${max} characters`
    }
    return true
  }
}

export const email = (value: string): boolean | string => {
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!pattern.test(value)) {
    return 'Must be a valid email address'
  }
  return true
}

export const number = (value: any): boolean | string => {
  if (isNaN(Number(value))) {
    return 'Must be a number'
  }
  return true
}

export const positiveNumber = (value: any): boolean | string => {
  if (isNaN(Number(value)) || Number(value) <= 0) {
    return 'Must be a positive number'
  }
  return true
}

export const skuValidator = (value: string): boolean | string => {
  if (!/^[A-Z0-9-]+$/.test(value)) {
    return 'SKU can only contain uppercase letters, numbers, and hyphens'
  }
  return true
}