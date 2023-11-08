package com.brascolor.brascolor;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam; 
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.beans.factory.annotation.Autowired;


@Controller

public class BrascolorController {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    
    @GetMapping("/login")
    public String login(@ModelAttribute("user") User user){
        if(user.isLoggedIn()){
            return "redirect:/"; 
        }
        return "components/login";
    }

    @PostMapping("/login")
    public String login(@RequestParam("idFunc") String username, @RequestParam("password") String pwd, @ModelAttribute("user") User user){
        if(user.isLoggedIn()){
            return "redirect:/"; 
        }
        if(username.equals("admin@test.com") && pwd.equals("admin")){
            user.setLoggedIn(true);
            return "redirect:/"; 
        }
        return "components/login";
    }

    @GetMapping("/")
    public String home() { 
        return "components/home";
    }
}
