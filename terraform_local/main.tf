resource "aws_instance" "decide" {
  ami                         = "ami-007fae589fdf6e955" # Amazon Linux 2 AMI (HVM), SSD Volume Type
  instance_type               = "t2.medium" # medium = 4Gb RAM
  associate_public_ip_address = true
  key_name                    = var.key_name
  vpc_security_group_ids      = [aws_security_group.sg_decide.id]

  root_block_device {
    volume_size = 20 #20 Gb
  }

  tags = {
    Name        = "${var.author}.decide.trebujena"
    Author      = var.author
    Date        = "2023.01.29"
    Environment = "LAB"
    Location    = "Paris"
    Project     = "decide"
  }

  connection {
    type        = "ssh"
    host        = self.public_ip
    user        = "ec2-user"
    private_key = file(var.key_path)
  }

  provisioner "remote-exec" {
    inline = [
      "sudo yum update -y",
      "sudo yum install -y docker httpd-tools",
      "sudo usermod -a -G docker ec2-user",
      "sudo curl -L https://github.com/docker/compose/releases/download/1.22.0-rc2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose",
      "sudo chmod +x /usr/local/bin/docker-compose",
      "sudo chkconfig docker on",
      "sudo service docker start",
      "mkdir /home/ec2-user/docker"
   ]
  }

  provisioner "file" {
    source      = "../docker/docker-compose.yml"
    destination = "/home/ec2-user/docker-compose.yml"
  }
  provisioner "file" {
    source      = "../docker/Dockerfile"
    destination = "/home/ec2-user/docker/Dockerfile"
  }
  provisioner "file" {
    source      = "../docker/Dockerfile-nginx"
    destination = "/home/ec2-user/docker/Dockerfile-nginx"
  }
  provisioner "file" {
    source      = "../docker/docker-nginx.conf"
    destination = "/home/ec2-user/docker/docker-nginx.conf"
  }
  provisioner "file" {
    source      = "../docker/docker-settings.py"
    destination = "/home/ec2-user/docker/docker-settings.py"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo /usr/local/bin/docker-compose up -d",
      "free"
    ]
  }
}
