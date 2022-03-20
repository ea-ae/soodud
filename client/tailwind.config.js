 module.exports = {
    //content: ["./src/**/*.{html,js}"],
    purge: {
        content: ['./src/**/*.{html,js,jsx,ts,tsx}'], // /dist/
        options: {
            safelist: []
        }
    },
    theme: {
        extend: {},
        fontFamily: {
            'roboto': 'Roboto, sans-serif',
        },
    },
    plugins: [],
}
