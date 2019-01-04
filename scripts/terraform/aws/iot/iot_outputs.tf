output "aws_iot_certificate_arn" {
  value = "${aws_iot_certificate.this.arn}"
}
output "aws_iot_policy_name" {
  value = "${aws_iot_policy.this.policy}"
}
output "aws_iot_policy" {
  value = "${aws_iot_policy.this.policy}"
}
output "aws_iot_thing_name" {
  value = "${aws_iot_thing.this.name}"
}
output "aws_iot_thing_id" {
  value = "${aws_iot_thing.this.id}"
}
output "aws_iot_endpoint_address" {
  value = "${data.aws_iot_endpoint.this.endpoint_address}"
}