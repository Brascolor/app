package com.brascolor.brascolor;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam; 
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;  

@RestController
public class BrascolorController { 
  
    @GetMapping("/")
    @RequestMapping(
        method = {RequestMethod.GET},
        value = {"/home"})
    @ResponseBody 
    public String home() { 
        return "home";
    }
}
