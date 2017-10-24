'use strict';

const fs = require('fs');

const envConfig = {
	'WIT_AI_ACCESS_TOKEN': process.env.WIT_AI_ACCESS_TOKEN,
	'TELEGRAM_ACCESS_TOKEN': process.env.TELEGRAM_ACCESS_TOKEN,
};

/* eslint-disable */

fs.writeFileSync( 'config.local.json', JSON.stringify( envConfig, null, 2 ) );
console.log('✅ Generated config.local.json');

