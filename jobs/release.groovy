job("nextchef-deploy-release") {
    label("nextchef-prod")
    steps {
        shell("""
sudo rm -fr *
sudo rm -fr .git
sudo rm -fr .gitignore
""")
        copyArtifacts('nextchef-build-app') {
            includePatterns("*/**")
            fingerprintArtifacts(false)
            buildSelector {
                upstreamBuild()
            }
        }
        shell("""
cd backend_project && sudo ./release.sh docker.apiumtech.io
""")
    }
    publishers {
        mailer("thuy.le@apiumtech.com, jose.barroso@apiumtech.com, binh.tran@apiumtech.com, rafa.hidalgo@apiumtech.com, lam.pham@apiumtech.com, rost.tok@apiumtech.com, oscar.galindo@apiumtech.com, sergi.fernandez@apiumtech.com", true, true)
    }
}
