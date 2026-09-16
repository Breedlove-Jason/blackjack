import {rmSync, mkdirSync, cpSync, copyFileSync} from 'node:fs';
rmSync('dist', {recursive:true, force:true}); mkdirSync('dist');
cpSync('web', 'dist', {recursive:true}); copyFileSync('engine.py', 'dist/engine.py');
