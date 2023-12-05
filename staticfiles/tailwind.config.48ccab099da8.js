module.exports = {
  tailwind.config = {
    theme: {
      extend: {
        colors: {
          primary: '#974067',
          primaryContainer: '#FFD9E4',
          onPrimaryContainer: '#3E0021',
          background: '#FFFBFF',
        },
        buttonPrimary: {
          display: 'flex',
          padding: '0.625rem 1.5rem',
          justifyContent: 'center',
          alignItems: 'center',
          gap: '0.5rem',
          flex: '1 0 0',
        },
      },
    },
  };
}
