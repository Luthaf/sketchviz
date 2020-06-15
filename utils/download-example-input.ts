import * as fs from 'fs';
import * as tmp from 'tmp';
import * as childProcess from 'child_process';

const tmpdir = tmp.dirSync({unsafeCleanup: true});
const checkout = tmpdir.name + '/chemiscope';

childProcess.execSync(
    'git clone https://github.com/cosmo-epfl/chemiscope' +
    ' --depth=1 ' + ' --branch=gh-pages ' + checkout
);

for (const file of ['CSD-500.json.gz', 'Arginine-Dipeptide.json.gz', 'Qm7b.json.gz', 'Azaphenacenes.json.gz', 'Zeolites.json.gz']) {
    fs.renameSync(`${checkout}/${file}`, `./app/${file}`);
}

fs.mkdirSync('./app/structures/', {recursive: true});
for (let i=0; i<523; i++) {
    const file = `Azaphenacenes-${i}.json`
    fs.renameSync(`${checkout}/structures/${file}`, `./app/structures/${file}`);
}

tmpdir.removeCallback();
