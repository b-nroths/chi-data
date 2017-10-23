cd frontend && npm run build
aws s3 sync build/ s3://chicago.bnroths.com --delete
# cd ..
# cd backend && chalice deploy
# cd ..
cd crons && serverless deploy
echo "http://chicago.bnroths.com"