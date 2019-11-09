#!/bin/bash
echo -n 'Commit Message ->'
read commit
git pull

cp -var /var/www/test.com/html /home/boyanm/training-projects/boyanM-RegForm-Apache2/
cp -var /usr/lib/cgi-bin/ /home/boyanm/training-projects/boyanM-RegForm-Apache2/

git add boyanM-RegForm-Apache2/
git commit -m "$commit"
git push
