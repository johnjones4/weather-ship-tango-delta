package main

import (
	"bytes"
	"encoding/json"
	"os"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
)

func publishWeather(w Weather) error {
	jsonBytes, err := json.Marshal(w)
	if err != nil {
		return err
	}

	sess := session.Must(session.NewSession())

	svc := s3.New(sess, &aws.Config{Region: aws.String("us-east-1")})

	bucket := aws.String(os.Getenv("S3_BUCKET"))

	_, err = svc.PutObject(&s3.PutObjectInput{
		Bucket: bucket,
		Key:    aws.String("latest.json"),
		ACL:    aws.String("public-read"),
		Body:   bytes.NewReader(jsonBytes),
	})

	return err
}
