import { definePreset } from '@primeuix/themes';
import Aura from '@primeuix/themes/aura';

const Noir = definePreset(Aura, {
    semantic: {
        primary: {
            50: '#f1f8e9',
            100: '#dcedc8',
            200: '#c5e1a5',
            300: '#aed581',
            400: '#9ccc65',
            500: '#8bc34a',
            600: '#7cb342',
            700: '#6AB23D',  // ваш основной цвет
            800: '#5a9e2e',
            900: '#4a8a20',
            950: '#3a7612'
        },
        colorScheme: {
            light: {
                primary: {
                    color: '{primary.700}',      // #6AB23D - основной цвет
                    contrastColor: '#ffffff',     // белый для контраста
                    hoverColor: '{primary.600}',  // #7cb342 - при наведении
                    activeColor: '{primary.800}'  // #5a9e2e - при нажатии
                },
                highlight: {
                    background: '{primary.700}',  // #6AB23D
                    focusBackground: '{primary.500}', // #8bc34a
                    color: '#ffffff',
                    focusColor: '#ffffff'
                }
            },
            dark: {
                primary: {
                    color: '{primary.300}',      // #aed581 - светлый зеленый для темной темы
                    contrastColor: '{primary.950}', // #3a7612 - темный для контраста
                    hoverColor: '{primary.200}',  // #c5e1a5
                    activeColor: '{primary.100}'  // #dcedc8
                },
                highlight: {
                    background: '{primary.300}',  // #aed581
                    focusBackground: '{primary.200}', // #c5e1a5
                    color: '{primary.950}',       // #3a7612
                    focusColor: '{primary.950}'
                }
            }
        }
    }
});

export default Noir;