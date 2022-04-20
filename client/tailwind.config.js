 module.exports = {
    // content: ["./src/**/*.{html,js,jsx,ts,tsx}"],
    important: true,
    purge: {
        content: ['./src/**/*.{html,js,jsx,ts,tsx}'], // /dist/
        options: {
            safelist: []
        }
    },
    theme: {
        extend: {
            screens: {
                'sm': '520px', // was 480
            },
        },
        fontFamily: {
            'main': 'Nunito, sans-serif',
        },
    },
    plugins: [],
}
