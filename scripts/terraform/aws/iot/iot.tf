#--------------------------------------------------------------------------------
# Unique endpoint specific to the AWS account making the call.
#--------------------------------------------------------------------------------
data "aws_iot_endpoint" "this" {}

#--------------------------------------------------------------------------------
# Sign CSR
# [Overview]
# To verify the device that accesses AWS IoT is legitimate, a client certificate
# signed by AWS IoT is required.
#
# [Prerequisite]
# CSR file "iot.csr" in scripts/terraform/aws/iot/pki directory.
#
# [How do I create self-signed device certificates to authenticate my devices with AWS IoT?]
# https://aws.amazon.com/premiumsupport/knowledge-center/iot-self-signed-certificates/
#--------------------------------------------------------------------------------
resource "aws_iot_certificate" "this" {
  csr    = "${file("${local.module_path}/pki/iot.csr")}"
  active = true
}

resource "aws_iot_policy" "this" {
  name = "${var.PROJECT}_${var.ENV}_allow_iot_${var.iot_thing_name}"
  policy = "${data.aws_iam_policy_document.this.json}"
}
data "aws_iam_policy_document" "this" {
  statement {
    sid    = "${title(var.PROJECT)}${title(var.ENV)}Allow${title(var.iot_thing_name)}AccessIoT"
    effect = "Allow"
    actions = ["iot:*"]
    resources = [
      "*"
    ]
  }
}
resource "aws_iot_policy_attachment" "this" {
  policy = "${aws_iot_policy.this.name}"
  target = "${aws_iot_certificate.this.arn}"
}

resource "aws_iot_thing" "this" {
  name = "${var.iot_thing_name}"

  attributes {
    Description = "${var.iot_thing_description}"
  }
}
resource "aws_iot_thing_principal_attachment" "att" {
  principal = "${aws_iot_certificate.this.arn}"
  thing     = "${aws_iot_thing.this.name}"
}