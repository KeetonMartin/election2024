export const formatDate = (timestamp: number): string => {
  console.log('timestamp', timestamp)
    return new Date(timestamp).toLocaleDateString("en-US", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  };
  
  export const formatPercentage = (value: number): string => {
    return `${value.toFixed(2)}%`;
  };